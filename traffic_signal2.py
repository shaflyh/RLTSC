import traci
import copy
import re
from config.signal_config import signal_configs
from typing import List
from networkdata import NetworkData
import json


def create_yellows(phases, yellow_length):
    new_phases = copy.copy(phases)
    yellow_dict = {}    # current phase + next phase keyed to corresponding yellow phase index
    # Automatically create yellow phases, traci will report missing phases as it assumes execution by index order
    for i in range(0, len(phases)):
        for j in range(0, len(phases)):
            if i != j:
                need_yellow, yellow_str = False, ''
                for sig_idx in range(len(phases[i].state)):
                    if (phases[i].state[sig_idx] == 'G' or phases[i].state[sig_idx] == 'g') and (phases[j].state[sig_idx] == 'r' or phases[j].state[sig_idx] == 's'):
                        need_yellow = True
                        yellow_str += 'y'
                    else:
                        yellow_str += phases[i].state[sig_idx]
                if need_yellow:  # If a yellow is required
                    new_phases.append(traci.trafficlight.Phase(yellow_length, yellow_str))
                    yellow_dict[str(i) + '_' + str(j)] = len(new_phases) - 1  # The index of the yellow phase in SUMO
    return new_phases, yellow_dict


class Signal:
    # Default min gap of SUMO (see https://sumo.dlr.de/docs/Simulation/Safety.html). Should this be parameterized?
    # MIN_GAP = 2.5
    
    def __init__(self, map_name, sumo, id, yellow_length, phases):
        self.sumo = sumo
        self.id = id
        self.yellow_time = yellow_length
        self.next_phase = 0
        self.max_green_time = 90
        self.min_green_time = 10
        self.phase_start_time = self.sumo.simulation.getTime()

        # Get traffic light information from this command instead
        self.lanes = list(
            dict.fromkeys(self.sumo.trafficlight.getControlledLanes(self.id))
        )  # Remove duplicates and keep order

        self.waiting_times = dict()     # SUMO's WaitingTime and AccumulatedWaiting are both wrong for multiple signals

        self.phases, self.yellow_dict = create_yellows(phases, yellow_length)

        programs = self.sumo.trafficlight.getAllProgramLogics(self.id)
        logic = programs[0]
        logic.type = 0
        logic.phases = self.phases
        self.sumo.trafficlight.setProgramLogic(self.id, logic)

        self.signals = None     # Used to allow signal sharing
        self.full_observation = None
        self.last_step_vehicles = None
        
        net_file = f'environments/{map_name}/{map_name}.net.xml'
        nd = NetworkData(net_file)
        self.netdata = nd.get_net_data()
        
        self.density_in_maxflow = 1#veh/km
        self.pressure = 0


    @property
    def phase(self):
        return self.sumo.trafficlight.getPhase(self.id)

    def prep_phase(self, new_phase):
        current_time = self.sumo.simulation.getTime()
        elapsed_time = current_time - self.phase_start_time
        # print(self.id)
        # print(current_time)
        # print(elapsed_time)
        # print(new_phase)
        
        if elapsed_time >= self.max_green_time:
            self.next_phase = (self.phase + 1) % len(self.phases)
            key = str(self.phase) + '_' + str(new_phase)
            if key in self.yellow_dict:
                yel_idx = self.yellow_dict[key]
                self.sumo.trafficlight.setPhase(self.id, yel_idx)  # turns yellow
            self.phase_start_time = current_time  # Reset phase start time when switching phases
        elif self.phase == new_phase:
            self.next_phase = self.phase
        elif elapsed_time <= self.min_green_time:
            self.next_phase = self.phase
        else:
            self.next_phase = new_phase
            key = str(self.phase) + '_' + str(new_phase)
            if key in self.yellow_dict:
                yel_idx = self.yellow_dict[key]
                self.sumo.trafficlight.setPhase(self.id, yel_idx)  # turns yellow
            self.phase_start_time = current_time  # Reset phase start time when switching phases

    def set_phase(self):
        self.sumo.trafficlight.setPhase(self.id, int(self.next_phase))

    def observe(self, step_length, distance):
        full_observation = dict()
        all_vehicles = set()
        for lane in self.lanes:
            vehicles = []
            lane_measures = {'queue': 0, 'approach': 0, 'total_wait': 0, 'max_wait': 0}
            lane_vehicles = self.get_vehicles(lane, distance)
            for vehicle in lane_vehicles:
                all_vehicles.add(vehicle)
                # Update waiting time
                if vehicle in self.waiting_times:
                    self.waiting_times[vehicle] += step_length
                elif self.sumo.vehicle.getWaitingTime(vehicle) > 0:  # Vehicle stopped here, add it
                    self.waiting_times[vehicle] = self.sumo.vehicle.getWaitingTime(vehicle)

                vehicle_measures = dict()
                vehicle_measures['id'] = vehicle
                vehicle_measures['wait'] = self.waiting_times[vehicle] if vehicle in self.waiting_times else 0
                vehicle_measures['speed'] = self.sumo.vehicle.getSpeed(vehicle)
                vehicle_measures['acceleration'] = self.sumo.vehicle.getAcceleration(vehicle)
                vehicle_measures['position'] = self.sumo.vehicle.getLanePosition(vehicle)
                vehicle_measures['type'] = self.sumo.vehicle.getTypeID(vehicle)
                vehicles.append(vehicle_measures)
                if vehicle_measures['wait'] > 0:
                    lane_measures['total_wait'] = lane_measures['total_wait'] + vehicle_measures['wait']
                    lane_measures['queue'] = lane_measures['queue'] + 1
                    if vehicle_measures['wait'] > lane_measures['max_wait']:
                        lane_measures['max_wait'] = vehicle_measures['wait']
                else:
                    lane_measures['approach'] = lane_measures['approach'] + 1
            lane_measures['vehicles'] = vehicles
            full_observation[lane] = lane_measures

        full_observation['num_vehicles'] = all_vehicles
        if self.last_step_vehicles is None:
            full_observation['arrivals'] = full_observation['num_vehicles']
            full_observation['departures'] = set()
        else:
            full_observation['arrivals'] = all_vehicles.difference(self.last_step_vehicles)
            departs = self.last_step_vehicles.difference(all_vehicles)
            full_observation['departures'] = departs
            # Clear departures from waiting times
            for vehicle in departs:
                if vehicle in self.waiting_times: self.waiting_times.pop(vehicle)

        self.last_step_vehicles = all_vehicles
        self.full_observation = full_observation
        self.pressure = self.get_pressure()

    # Remove undetectable vehicles from lane
    def get_vehicles(self, lane, max_distance):
        detectable = []
        for vehicle in self.sumo.lane.getLastStepVehicleIDs(lane):
            path = self.sumo.vehicle.getNextTLS(vehicle)
            if len(path) > 0:
                next_light = path[0]
                distance = next_light[2]
                if distance <= max_distance:  # Detectors have a max range
                    detectable.append(vehicle)
        return detectable

    def get_pressure(self): #get weight = pressure/lane lenght
        mp_lanes = self.max_pressure_lanes() #inc & out lanes for each phase
        # print(mp_lanes)
        pressure = {}
        for phase in mp_lanes:
            in_out_lanes = mp_lanes[phase]

            inc_lanes = in_out_lanes['inc']
            veh_in_inc = sum((self.sumo.lane.getLastStepVehicleNumber(l)/self.sumo.lane.getLength(l)) for l in inc_lanes)

            out_lanes = in_out_lanes['out']
            veh_in_out = sum((self.sumo.lane.getLastStepVehicleNumber(k)/self.sumo.lane.getLength(k)) for k in out_lanes)

            pressure[phase] = abs(veh_in_inc - veh_in_out)/self.density_in_maxflow
        pressure_total = sum(pressure.values())
        return pressure_total
    
    def get_tl_green_phases(self):
        logic = self.sumo.trafficlight.getAllProgramLogics(self.id)[0]
        
        #get only the green phases
        green_phases = [ p.state for p in logic.getPhases()
                         if 'y' not in p.state
                         and ('G' in p.state or 'g' in p.state) ]

        #sort to ensure parity between sims (for RL actions)
        return sorted(green_phases)
    
    def phase_lanes(self, actions):
        phase_lanes = {a:[] for a in actions}
        for a in actions:
            green_lanes = set()
            red_lanes = set()
            for s in range(len(a)):
                if a[s] == 'g' or a[s] == 'G':
                    green_lanes.add(self.netdata['inter'][self.id]['tlsindex'][s])
                elif a[s] == 'r':
                    red_lanes.add(self.netdata['inter'][self.id]['tlsindex'][s])

            ###some movements are on the same lane, removes duplicate lanes
            pure_green = [l for l in green_lanes if l not in red_lanes]
            if len(pure_green) == 0:
                phase_lanes[a] = list(set(green_lanes))
            else:
                phase_lanes[a] = list(set(pure_green))
        return phase_lanes
    
    def max_pressure_lanes(self):
        """for each green phase, get all incoming
        and outgoing lanes for that phase, store
        in dict for max pressure calculation
        """
        green_phases = self.get_tl_green_phases()
        phase_lanes2 = self.phase_lanes(green_phases)
        max_pressure_lanes = {}
        for g in green_phases:
            inc_lanes = set()
            out_lanes = set()
            for l in phase_lanes2[g]:
                inc_lanes.add(l)
                for ol in self.netdata['lane'][l]['outgoing']:
                    out_lanes.add(ol)

            max_pressure_lanes[g] = {'inc':inc_lanes, 'out':out_lanes}

        #print("mp_lanes :", str(max_pressure_lanes))
        return max_pressure_lanes
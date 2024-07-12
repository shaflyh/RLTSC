import matplotlib.pyplot as plt
import pandas as pd
import datetime
import math

csv_lanelength = 'environments/jakarta/lane-length-new.csv'
csv_list = ['lanedata_jakarta_fixed.csv',]
# csv_list = ['lane_ids.csv']
# print(csv_lanelength)
# print(csv_list[0])


def get_lane_length(csv_lanelength):  # get lane length information
    lanelength_data = pd.read_csv(csv_lanelength, skiprows=1, header=None)
    # print(lanelength_data)
    lane_list = lanelength_data[0]
    length_list = lanelength_data[1]/1000
    # store in dictionary :
    lane_length = dict(zip(lane_list, length_list))
    return lane_length


def get_data_group(csv_flow_and_density):  # grouping data to pandas object
    # get flow(veh/hr) and density(veh/km) in each lane for certain interval
    flowdensity = pd.read_csv(csv_flow_and_density, delimiter=';', header=0)
    print(flowdensity.head())

    # only for get a list of 'time' in mfd-data.csv
    flowdensity_lane = flowdensity.groupby('lane_id')
    dummy_group = flowdensity_lane.get_group(
        list(flowdensity_lane.groups.keys())[0])
    time_list = dummy_group['time']
    # print(time_list)

    # real grouping (group by time)
    flowdensity_time = flowdensity.groupby('time')
    return time_list, flowdensity_time


def get_MFD_property(time_list, flowdensity_time, total_lane_length, lane_length_dict):  # calculate Qt and Kt
    Q = []  # list of network flow
    K = []  # list of network density
    # calculate network flow (Qt) and network density(Kt)
    for time in time_list[::]:
        the_group = flowdensity_time.get_group(time)
        lane_ids = the_group['lane_id']
        lane_flows = the_group['outflow']
        lane_densities = the_group['laneDensity']
        flowx = []
        densityx = []
        # bisa dibenerin tanpa enumerate
        for i, lane in enumerate(lane_ids):
            lane_id = lane_ids.iloc[i]
            lane_flow = lane_flows.iloc[i]
            lane_density = lane_densities.iloc[i]
            # get lane length from earlier dictionary in lane-length.csv
            lane_length = lane_length_dict[str(lane_id)]

            if (math.isnan(lane_density)):
                lane_density = 0
            flowxlength = lane_flow*lane_length
            flowx.append(flowxlength)  # list
            densityxlength = lane_density*lane_length
            # print(lane_density)
            densityx.append(densityxlength)  # list
        Qt = sum(flowx)/total_lane_length
        Kt = sum(densityx)/total_lane_length
        # print(sum(densityx))
        Q.append(Qt)
        K.append(Kt)
    return Q, K


def convert(n):
    return str(datetime.timedelta(seconds=n))


lane_length_dict = get_lane_length(csv_lanelength)
# total lane length in network (KM)
total_lane_length = sum(lane_length_dict.values())

time_list = {}
flowdensity_time = {}
Qn = {}
Kn = {}

for i, csv in enumerate(csv_list):
    time_list[csv], flowdensity_time[csv] = get_data_group(csv)
    Qn[i], Kn[i] = get_MFD_property(
        time_list[csv], flowdensity_time[csv], total_lane_length, lane_length_dict)
    # Qn flow, Kn density
# print(len(Kn['lane_ids.xlsx']))
# density_flow_csv = 'flow-density-csv/density_flow.csv'
# print(len(Qn[0]))


time_list_hr = {}
for csv in csv_list:
    time_list_hr[csv] = [0]

for csv in csv_list:
    for time_s in time_list[csv]:
        time_list_hr[csv].append(convert(time_s))

for csv in csv_list:
    time_list_hr[csv].pop(0)


list_interval = 2
ticks_list = [str(n)+':00:00' for n in range(6, 24, list_interval)]

ticks_list_y = [d for d in range(0, 250, 50)]



for i, csv in enumerate(csv_list):
    print(sum(Kn[i]))
    print(max(Kn[i]))
    print(sum(Qn[i]))
    print(max(Qn[i]))
    plt.scatter(Kn[i], Qn[i], label=csv, s=5)
plt.yticks(ticks_list_y)
plt.title('Macroscopic Fundamental Diagram')
plt.xlabel('Network Density (veh/km)')
plt.ylabel('Network Flow (veh/hr)')
plt.legend(loc='upper right', frameon=False)
plt.show()


'''
#plot flow vs time
#plt.scatter(time_list_hr_4,Q_4,color='red',label='Webster')
#plt.scatter(time_list_hr_2,Q_2, color='brown',label='Q-Learning')
plt.scatter(time_list_hr_5n,Q_5,color='black',label='DQN')
plt.xticks(ticks_list, rotation = 45)
#plt.scatter(time_list_hr_1,Q_1, color='lightcoral',label='Fixed-Time')
#plt.scatter(time_list_hr_3,Q_3,color='cornflowerblue',label='Max-Pressure')
plt.title('Flow vs Time')
plt.xlabel('Simulation time')
plt.ylabel('Network Flow (veh/hr)')
plt.legend(loc='upper right', frameon=False)
plt.show()
'''


# plot density vs time
# plt.style.use('fivethirtyeight')
# plt.scatter(time_list_hr['mfd-data-wb.csv'],Kn['mfd-data-wb.csv'],color='red',label='Webster')
# plt.scatter(time_list_hr['MP/mfd-data-MP-length-last-3.csv'],Kn['MP/mfd-data-MP-length-last-3.csv'],color='dodgerblue',label='Max-Pressure N = 1') # N = 1
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman.csv'],Kn['mfd-data-dqn-boltzman.csv'],color='black',label='DQN-boltzman-reward = 1-(0.5 0.5)')
# plt.scatter(time_list_hr['MP/mfd-data-MP-length-2.csv'],Kn['MP/mfd-data-MP-length-2.csv'],color='dodgerblue',label='Max-Pressure')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-0.1-0.9.csv'],Kn['mfd-data-dqn-boltzman-weight-0.1-0.9.csv'],color='blue',label='DQN-boltzman-reward = -(0.1 0.9)')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-1-(0.3-0.7).csv'],Kn['mfd-data-dqn-boltzman-weight-1-(0.3-0.7).csv'],color='rebeccapurple',label='DQN-boltzman-reward = 1-(0.3 0.7)')
# plt.scatter(time_list_hr['mfd-data-uniform-20.csv'],Kn['mfd-data-uniform-20.csv'],color='steelblue',label='Uniform 20s')
# plt.scatter(time_list_hr['mfd-data-uniform-25.csv'],Kn['mfd-data-uniform-25.csv'],color='rebeccapurple',label='Uniform 25s')
# plt.scatter(time_list_hr['mfd-data-uniform-30.csv'],Kn['mfd-data-uniform-30.csv'],color='midnightblue',label='Uniform 30s')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-0.9-0.1.csv'],Kn['mfd-data-dqn-boltzman-weight-0.9-0.1.csv'],color='midnightblue',marker='D',label='DQN-boltzman-reward = -(0.9 0.1)')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-0.7-0.3.csv'],Kn['mfd-data-dqn-boltzman-weight-0.7-0.3.csv'],color='forestgreen',marker='*',label='DQN-boltzman-reward = -(0.7 0.3)')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-0.5-0.5.csv'],Kn['mfd-data-dqn-boltzman-weight-0.5-0.5.csv'],color='darkgrey',marker='s',label='DQN-boltzman-reward = -(0.5 0.5)')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-0.3-0.7.csv'],Kn['mfd-data-dqn-boltzman-weight-0.3-0.7.csv'],color='rebeccapurple',marker='^',label='DQN-boltzman-reward = -(0.3 0.7)')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-weight-0.1-0.9-2.csv'],Kn['mfd-data-dqn-boltzman-weight-0.1-0.9-2.csv'],color='blue',marker='X',label='DQN-boltzman-reward = -(0.1 0.9)')


# plt.scatter(time_list_hr['mfd-data-dqn-epsilon-reward-pressure-state-1-2.csv' ],Kn['mfd-data-dqn-epsilon-reward-pressure-state-1-2.csv'],color='blue',label='DQN-epsilon-state 1-reward = -pressure')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzmann-reward-pressure-state-1.csv' ],Kn['mfd-data-dqn-boltzmann-reward-pressure-state-1.csv' ],color='crimson',label='DQN-boltzman-state 1-reward = -pressure')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-pressure.csv'],Kn['mfd-data-dqn-boltzman-pressure.csv'],color='orange',label='DQN-boltzman-state 2-reward = -pressure')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-queue.csv'],Kn['mfd-data-dqn-boltzman-queue.csv'],color='teal',label='DQN-boltzman-reward = -queue')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-min-exponen-K=25.csv'],Kn['mfd-data-dqn-boltzman-min-exponen-K=25.csv'],color='black',label='DQN-boltzman-reward = -exponen ') #K = 25
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-min-exponen-K=18.csv'],Kn['mfd-data-dqn-boltzman-min-exponen-K=18.csv'],color='royalblue',label='DQN-boltzman-reward = -exponen K = 18')
# plt.scatter(time_list_hr['mfd-data-dqn-boltzman-min-exponen-K=25-bootstrap.csv'],Kn['mfd-data-dqn-boltzman-min-exponen-K=25-bootstrap.csv'],color='blue',label='DQN-boltzman-bootstrap-reward = -exponen') #K = 25

'''salah, no maxgreen
#plt.scatter(time_list_hr['MP/mfd-data-MP-no-length-last.csv'],Kn['MP/mfd-data-MP-no-length-last.csv'],color='midnightblue',label='Max-Pressure ...(1)')
#plt.scatter(time_list_hr['MP/mfd-data-MP-length-last.csv'],Kn['MP/mfd-data-MP-length-last.csv'],color='steelblue',label='Max-Pressure ...(2)')
#plt.scatter(time_list_hr['MP/mfd-data-MP-length-last-2.csv'],Kn['MP/mfd-data-MP-length-last-2.csv'],color='dodgerblue',label='Max-Pressure ...(2)')
'''

# plt.scatter(time_list_hr['MP/mfd-data-MP-no-length-last-3.csv'],Kn['MP/mfd-data-MP-no-length-last-3.csv'],color='midnightblue',label='Max-Pressure ...(1)')

'''
plt.scatter(time_list_hr['MP/mfd-data-MP-length-N=2.csv'],Kn['MP/mfd-data-MP-length-N=2.csv'],color='rebeccapurple',marker='D',label='Max-Pressure N = 2')
plt.scatter(time_list_hr['MP/mfd-data-MP-length-N=3.csv'],Kn['MP/mfd-data-MP-length-N=3.csv'],color='midnightblue',marker='*',label='Max-Pressure N = 3')
plt.scatter(time_list_hr['MP/mfd-data-MP-length-N=4.csv'],Kn['MP/mfd-data-MP-length-N=4.csv'],color='blue',marker='s',label='Max-Pressure N = 4')
plt.scatter(time_list_hr['MP/mfd-data-MP-length-N=5.csv'],Kn['MP/mfd-data-MP-length-N=5.csv'],color='steelblue',marker='X',label='Max-Pressure N = 5')
'''

# plt.scatter(time_list_hr['mfd-data-dqn-epsilon-reward-pressure-state-1.csv'],Kn['mfd-data-dqn-epsilon-reward-pressure-state-1.csv'],color='blue',label='DQN-epsilon-reward = -pressure') # state - 1
# plt.scatter(time_list_hr['mfd-data-dqn-epsilon-reward-pressure-state-2.csv'],Kn['mfd-data-dqn-epsilon-reward-pressure-state-2.csv'],color='grey',label='DQN-epsilon-state 2-reward = -pressure ') #state - 2
'''
plt.xticks(ticks_list)
plt.title('Density vs Time')
plt.xlabel('Simulation time')
plt.ylabel('Network Density (veh/km)')
plt.legend(loc='lower right', frameon=False)
plt.show()
'''

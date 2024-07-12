import pathlib
import os
import multiprocessing as mp


from multi_signal import MultiSignal
import argparse
from config.agent_config import agent_configs
from config.map_config import map_configs
from config.mdp_config import mdp_configs
from adversarial import fgsm_attack, pgd_attack


import time
start_time = time.time()


def main():

    ap = argparse.ArgumentParser(
        description='Run traffic signal control simulations with various configurations.')
    ap.add_argument("--agent", type=str, default='STOCHASTIC',
                    # choices=['STOCHASTIC', 'MAXWAVE', 'MAXPRESSURE', 'IDQN', 'IDQN2', 'IPPO', 'MPLight', 'FMA2C',
                    #          'MPLightFULL', 'FMA2CFull', 'FMA2CVAL'],
                    help='Type of agent to use in the simulation.')
    ap.add_argument("--trials", type=int, default=1,
                    help='Number of simulation trials to run.')
    ap.add_argument("--eps", type=int, default=10000,
                    help='Number of episodes per trial.')
    ap.add_argument("--procs", type=int, default=1,
                    help='Number of processes to use for parallel execution. Set to 1 to run sequentially.')
    ap.add_argument("--map", type=str, default='ingolstadt1',
                    choices=['grid4x4', 'arterial4x4', 'ingolstadt1', 'ingolstadt7', 'ingolstadt21',
                             'cologne1', 'cologne3', 'cologne8', 'jakarta', 'jakarta1'],
                    help='The map configuration to use for the simulation.')
    ap.add_argument("--pwd", type=str, default=os.path.dirname(__file__),
                    help='Path to the directory where the script is located.')
    ap.add_argument("--log_dir", type=str, default=os.path.join(os.getcwd(), 'results' + os.sep),
                    help='Directory to save log files.')
    ap.add_argument("--gui", type=bool, default=False,
                    help='Boolean flag to turn on or off the graphical user interface.')
    ap.add_argument("--libsumo", type=bool, default=True,
                    help='Boolean flag to use libsumo (True) or Traci (False) as the backend. Note: libsumo does not support multi-threading.')
    ap.add_argument("--tr", type=int, default=0,
                    help='Trial number to run when multi-threading is not used.')
    ap.add_argument("--save_freq", type=int, default=100,
                    help='Frequency of saving the simulation state.')
    ap.add_argument("--load", type=bool, default=False,
                    help='Boolean flag to load the agent from a saved state.')
    # ap.add_argument("--robust", action='store_true', help="Robust training.")
    ap.add_argument("--attack", type=str, choices=['PGD', 'FSGM'],)
    ap.add_argument("--name", type=str, default='default', help='Additional folder name.')
    ap.add_argument("--fixed", action='store_true', help="Running with fixed time only.")
    

    args = ap.parse_args()

    if args.libsumo:
        # Set the environment variable
        os.environ['LIBSUMO_AS_TRACI'] = '1'
        
    if args.attack == 'FSGM':
        args.name = args.name + ' FSGM attack'
        print(args.name)
    if args.attack == 'PGD':
        args.name = args.name + ' PGD attack'
        
    # Check if libsumo installed
    if args.libsumo and 'LIBSUMO_AS_TRACI' not in os.environ:
        raise EnvironmentError(
            "Set LIBSUMO_AS_TRACI to nonempty value to enable libsumo. \nInstall libsumo (pip install libsumo) and (export LIBSUMO_AS_TRACI=1)")

    # Determine execution mode based on command line arguments
    if args.procs == 1 or args.libsumo:
        # run the simulation sequentially without multiprocessing.
        run_trial(args, args.tr)
    else:
        # use Python's multiprocessing to run trials in parallel.
        pool = mp.Pool(processes=args.procs)
        for trial in range(1, args.trials+1):
            pool.apply_async(run_trial, args=(args, trial))
        pool.close()
        pool.join()


def run_trial(args, trial):
    agt_config = agent_configs[args.agent]
    agt_config['save_freq'] = args.save_freq
    agt_config['load'] = args.load
    alg = agt_config['agent']
    
    ## MDP Config for FMA2C
    mdp_config = mdp_configs.get(args.agent)
    if mdp_config is not None:
        mdp_map_config = mdp_config.get(args.map)
        if mdp_map_config is not None:
            mdp_config = mdp_map_config
        mdp_configs[args.agent] = mdp_config
        
    if mdp_config is not None:
        agt_config['mdp'] = mdp_config
        management = agt_config['mdp'].get('management')
        if management is not None:    # Save some time and precompute the reverse mapping
            supervisors = dict()
            for manager in management:
                workers = management[manager]
                for worker in workers:
                    supervisors[worker] = manager
            mdp_config['supervisors'] = supervisors

    map_config = map_configs[args.map]
    num_steps_eps = int(
        (map_config['end_time'] - map_config['start_time']) / map_config['step_length'])
    route = map_config['route']
    if route is not None:
        route = os.path.join(args.pwd, route)
    if args.map == 'grid4x4' or args.map == 'arterial4x4':
        if not os.path.exists(route):
            raise EnvironmentError(
                "You must decompress environment files defining traffic flow")
            
    # TODO: Add paramater for number of trial
    env = MultiSignal(alg.__name__,
                      args.map,
                      os.path.join(args.pwd, map_config['net']),
                      agt_config['state'],
                      agt_config['reward'],
                      route=route, step_length=map_config['step_length'], yellow_length=map_config['yellow_length'],
                      step_ratio=map_config['step_ratio'], end_time=map_config['end_time'],
                      max_distance=agt_config['max_distance'], lights=map_config['lights'], gui=args.gui,
                      log_dir=os.path.join(args.log_dir, args.map), libsumo=args.libsumo, warmup=map_config['warmup'],
                      name=args.name
                      )
    
    if(args.fixed):
        for _ in range(args.eps):
            env.reset()
            print(f'Episode {_+1}')
            done = False
            while not done:
                obs, rew, done, info = env.step_fixed()
        finished
        

    # schedulers decay over 80% of steps
    agt_config['episodes'] = int(args.eps * 0.8)
    agt_config['steps'] = agt_config['episodes'] * num_steps_eps
    agt_config['log_dir'] = os.path.join(args.log_dir, args.map, env.connection_name)
    agt_config['num_lights'] = len(env.all_ts_ids)

    
    # Get agent id's, observation shapes, and action sizes from env
    obs_act = dict()
    for ts in env.obs_shape:
        obs_act[ts] = [env.obs_shape[ts], len(
            env.phases[ts]) if ts in env.phases else None]
        
    # print('\nAgent Parameters')
    # print(f'Agent config: \n {agt_config}')
    # print(f'\nObservation action: \n {obs_act}')
    # print(f'Map: {args.map}')
    # print(f'Thread number : {trial}\n')
    agent = alg(agt_config, obs_act, args.map, trial)

    for _ in range(args.eps):
        obs = env.reset()
        print(f'Episode {_+1}')
        done = False
        if args.attack == 'FSGM':
            print("FSGM Attack Env")
            while not done:
                epsilon = 1/20  # Define the strength of the perturbation
                # print(obs)
                perturbed_obs = fgsm_attack(agent, obs, epsilon)
                # print('perturbed_obs')
                # print(perturbed_obs)
                act = agent.act(perturbed_obs)
                obs, rew, done, info = env.step(act)
                agent.observe(obs, rew, done, info)
        elif args.attack == 'PGD':
            print("PGD Attack Env")
            while not done:
                epsilon = 5/100  # Define the strength of the perturbation
                perturbed_obs = pgd_attack(agent, obs, epsilon)
                act = agent.act(perturbed_obs)
                obs, rew, done, info = env.step(act)
                agent.observe(obs, rew, done, info)
        else:
            while not done:
                act = agent.act(obs)            
                obs, rew, done, info = env.step(act)
                agent.observe(obs, rew, done, info)
    env.close()

if __name__ == '__main__':
    main()


# Execution time
total = time.time() - start_time
h, remain = divmod(total, 3600)
m, s = divmod(remain, 60)
print(f"Execution time: {int(h)} hours {int(m)} minutes {s:.2f} seconds")

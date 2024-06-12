import rewards as rewards
import states as states

from agents.stochastic import STOCHASTIC
from agents.maxwave import MAXWAVE
from agents.maxpressure import MAXPRESSURE
from agents.pfrl_dqn import IDQN
from agents.pfrl_ppo import IPPO
from agents.mplight import MPLight
from agents.fma2c import FMA2C

agent_configs = {
    # *VAL configs have distance settings according to the validation scenarios
    'MAXWAVEVAL': {
        'agent': MAXWAVE,
        'state': states.wave,
        'reward': rewards.wait,
        'max_distance': 50
    },
    'MAXPRESSUREVAL': {
        'agent': MAXPRESSURE,
        'state': states.mplight,
        'reward': rewards.wait,
        'max_distance': 9999
    },
    'MPLightVAL': {
        'agent': MPLight,
        'state': states.mplight,
        'reward': rewards.pressure,
        'max_distance': 9999,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500,
        'demand_shape': 1
    },
    'FMA2CVAL': {
        'agent': FMA2C,
        'state': states.fma2c,
        'reward': rewards.fma2c,
        'max_distance': 50,
        'management_acts': 4,
        'rmsp_alpha': 0.99,
        'rmsp_epsilon': 1e-5,
        'max_grad_norm': 40,
        'gamma': 0.96,
        'lr_init': 2.5e-4,
        'lr_decay': 'constant',
        'entropy_coef_init': 0.001,
        'entropy_coef_min': 0.001,
        'entropy_decay': 'constant',
        'entropy_ratio': 0.5,
        'value_coef': 0.5,
        'num_lstm': 64,
        'num_fw': 128,
        'num_ft': 32,
        'num_fp': 64,
        'batch_size': 120,
        'reward_norm': 2000.0,
        'reward_clip': 2.0,
    },

    'STOCHASTIC': {
        'agent': STOCHASTIC,
        'state': states.mplight,
        'reward': rewards.wait,
        'max_distance': 1
    },
    'MAXWAVE': {
        'agent': MAXWAVE,
        'state': states.wave,
        'reward': rewards.wait,
        'max_distance': 50
    },
    'MAXPRESSURE': {
        'agent': MAXPRESSURE,
        'state': states.mplight,
        'reward': rewards.wait,
        'max_distance': 200
    },
    'IDQN': {
        'agent': IDQN,
        'state': states.drq_norm,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'MPLight': {
        'agent': MPLight,
        'state': states.mplight,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500,
        'demand_shape': 1
    },
    # Reward wait norm
    'IDQN1': {
        'agent': IDQN,
        'state': states.drq_norm,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN2': {
        'agent': IDQN,
        'state': states.queue,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN3': {
        'agent': IDQN,
        'state': states.approach,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN4': {
        'agent': IDQN,
        'state': states.speed,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN5': {
        'agent': IDQN,
        'state': states.drq_norm_rand,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN6': {
        'agent': IDQN,
        'state': states.queue_rand,
        'reward': rewards.wait_norm,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    # reward pressure
    'IDQN1P': {
        'agent': IDQN,
        'state': states.drq_norm,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN2P': {
        'agent': IDQN,
        'state': states.queue,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN3P': {
        'agent': IDQN,
        'state': states.approach,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN4P': {
        'agent': IDQN,
        'state': states.speed,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    # reward pressure rand
    'IDQN1PR': {
        'agent': IDQN,
        'state': states.drq_norm,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN2PR': {
        'agent': IDQN,
        'state': states.queue,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN3PR': {
        'agent': IDQN,
        'state': states.approach,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN4PR': {
        'agent': IDQN,
        'state': states.speed,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN5PR': {
        'agent': IDQN,
        'state': states.drq_norm_rand,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    'IDQN6PR': {
        'agent': IDQN,
        'state': states.queue_rand,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500
    },
    # reward pressure random
    'MPLightR': {
        'agent': MPLight,
        'state': states.mplight_rand,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500,
        'demand_shape': 1
    },
    'MPLightFULLR': {
        'agent': MPLight,
        'state': states.mplight_full_rand,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500,
        'demand_shape': 4
    },
    'IPPO': {
        'agent': IPPO,
        'state': states.drq_norm,
        'reward': rewards.wait_norm,
        'max_distance': 200
    },
    # Reward wait norm
    'IPPO1': {
        'agent': IPPO,
        'state': states.drq_norm,
        'reward': rewards.wait_norm,
        'max_distance': 200,
    },
    'IPPO2': {
        'agent': IPPO,
        'state': states.queue,
        'reward': rewards.wait_norm,
        'max_distance': 200,
    },
    'IPPO3': {
        'agent': IPPO,
        'state': states.approach,
        'reward': rewards.wait_norm,
        'max_distance': 200,
    },
    'IPPO4': {
        'agent': IPPO,
        'state': states.speed,
        'reward': rewards.wait_norm,
        'max_distance': 200,
    },
    'IPPO5': {
        'agent': IPPO,
        'state': states.drq_norm_rand,
        'reward': rewards.wait_norm,
        'max_distance': 200,
    },
    'IPPO6': {
        'agent': IPPO,
        'state': states.queue_rand,
        'reward': rewards.wait_norm,
        'max_distance': 200,
    },
    # reward pressure
    'IPPO1P': {
        'agent': IPPO,
        'state': states.drq_norm,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'TARGET_UPDATE': 500
    },
    'IPPO2P': {
        'agent': IPPO,
        'state': states.queue,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'TARGET_UPDATE': 500
    },
    'IPPO3P': {
        'agent': IPPO,
        'state': states.approach,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'TARGET_UPDATE': 500
    },
    'IPPO4P': {
        'agent': IPPO,
        'state': states.speed,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'TARGET_UPDATE': 500
    },
    # reward pressure rand
    'IPPO1PR': {
        'agent': IPPO,
        'state': states.drq_norm,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
    },
    'IPPO2PR': {
        'agent': IPPO,
        'state': states.queue,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
    },
    'IPPO3PR': {
        'agent': IPPO,
        'state': states.approach,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
    },
    'IPPO4PR': {
        'agent': IPPO,
        'state': states.speed,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
    },
    'IPPO5PR': {
        'agent': IPPO,
        'state': states.drq_norm_rand,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
    },
    'IPPO6PR': {
        'agent': IPPO,
        'state': states.queue_rand,
        'reward': rewards.pressure_rand,
        'max_distance': 200,
    },
    'FMA2C': {
        'agent': FMA2C,
        'state': states.fma2c,
        'reward': rewards.fma2c,
        'max_distance': 200,
        'management_acts': 4,
        'rmsp_alpha': 0.99,
        'rmsp_epsilon': 1e-5,
        'max_grad_norm': 40,
        'gamma': 0.96,
        'lr_init': 2.5e-4,
        'lr_decay': 'constant',
        'entropy_coef_init': 0.001,
        'entropy_coef_min': 0.001,
        'entropy_decay': 'constant',
        'entropy_ratio': 0.5,
        'value_coef': 0.5,
        'num_lstm': 64,
        'num_fw': 128,
        'num_ft': 32,
        'num_fp': 64,
        'batch_size': 120,
        'reward_norm': 2000.0,
        'reward_clip': 2.0,
    },

    # *FULL configs extend state space to include obs. available to IDQN
    'MPLightFULL': {
        'agent': MPLight,
        'state': states.mplight_full,
        'reward': rewards.pressure,
        'max_distance': 200,
        'BATCH_SIZE': 32,
        'GAMMA': 0.99,
        'EPS_START': 1.0,
        'EPS_END': 0.0,
        'EPS_DECAY': 220,
        'TARGET_UPDATE': 500,
        'demand_shape': 4
    },
    'FMA2CFULL': {
        'agent': FMA2C,
        'state': states.fma2c_full,
        'reward': rewards.fma2c_full,
        'max_distance': 200,
        'management_acts': 4,
        'rmsp_alpha': 0.99,
        'rmsp_epsilon': 1e-5,
        'max_grad_norm': 40,
        'gamma': 0.96,
        'lr_init': 2.5e-4,
        'lr_decay': 'constant',
        'entropy_coef_init': 0.001,
        'entropy_coef_min': 0.001,
        'entropy_decay': 'constant',
        'entropy_ratio': 0.5,
        'value_coef': 0.5,
        'num_lstm': 64,
        'num_fw': 128,
        'num_ft': 32,
        'num_fp': 64,
        'batch_size': 120,
        'reward_norm': 2000.0,
        'reward_clip': 2.0,
    }
}

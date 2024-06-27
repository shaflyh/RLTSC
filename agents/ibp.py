import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

def initial_bounds(x0, epsilon):
    '''
    x0 = input, b x c x h x w
    '''
    upper = x0+epsilon
    lower = x0-epsilon
    return upper, lower

def weighted_bound(layer, prev_upper, prev_lower):
    prev_mu = (prev_upper + prev_lower)/2
    prev_r = (prev_upper - prev_lower)/2
    mu = layer(prev_mu)
    if type(layer)==nn.Linear:
        r = F.linear(prev_r, torch.abs(layer.weight))
    elif type(layer)==nn.Conv2d:
        r = F.conv2d(prev_r, torch.abs(layer.weight), stride=layer.stride, padding=layer.padding)
    
    upper = mu + r
    lower = mu - r
    return upper, lower

def activation_bound(layer, prev_upper, prev_lower):
    upper = layer(prev_upper)
    lower = layer(prev_lower)
    return upper, lower

def network_bounds(model, x0, epsilon):
    '''
    get interval bound progation upper and lower bounds for the activation of a model
    
    model: a nn.Sequential module
    x0: input, b x input_shape
    epsilon: float, the linf distance bound is calculated over
    '''
    upper, lower = initial_bounds(x0, epsilon)
    for layer in model.modules():
        if type(layer) in (nn.Sequential,):
            pass
        elif type(layer) in (nn.ReLU, nn.Sigmoid, nn.Tanh, nn.MaxPool2d, nn.Flatten):
            upper, lower = activation_bound(layer, upper, lower)
        elif type(layer) in (nn.Linear, nn.Conv2d):
            upper, lower = weighted_bound(layer, upper, lower)
        else:
            print('Unsupported layer:', type(layer))
    return upper, lower

def subsequent_bounds(model, upper, lower):
    '''
    get interval bound progation upper and lower bounds for the activation of a model,
    given bounds of the input
    
    model: a nn.Sequential module
    upper: upper bound on input layer, b x input_shape
    lower: lower bound on input layer, b x input_shape
    '''
    for layer in model.modules():
        if type(layer) in (nn.Sequential,):
            pass
        elif type(layer) in (nn.ReLU, nn.Sigmoid, nn.Tanh, nn.MaxPool2d, nn.Flatten):
            upper, lower = activation_bound(layer, upper, lower)
        elif type(layer) in (nn.Linear, nn.Conv2d):
            upper, lower = weighted_bound(layer, upper, lower)
        else:
            print('Unsupported layer:', type(layer))
    return upper, lower

class EpsilonScheduler():
    def __init__(self, schedule_type, init_step, final_step, init_value, final_value, num_steps_per_epoch, mid_point=.25, beta=4.):
        self.schedule_type = schedule_type
        self.init_step = init_step
        self.final_step = final_step
        self.init_value = init_value
        self.final_value = final_value
        self.mid_point = mid_point
        self.beta = beta
        self.num_steps_per_epoch = num_steps_per_epoch
        assert self.final_value >= self.init_value
        assert self.final_step >= self.init_step
        assert self.beta >= 2.
        assert self.mid_point >= 0. and self.mid_point <= 1.

    def get_eps(self, epoch, step):
        if self.schedule_type == "smoothed":
            return self.smooth_schedule(epoch * self.num_steps_per_epoch + step, self.init_step, self.final_step, self.init_value, self.final_value, self.mid_point, self.beta)
        else:
            return self.linear_schedule(epoch * self.num_steps_per_epoch + step, self.init_step, self.final_step, self.init_value, self.final_value)

    # Smooth schedule that slowly morphs into a linear schedule.
    # Code is adapted from DeepMind's IBP implementation:
    # https://github.com/deepmind/interval-bound-propagation/blob/2c1a56cb0497d6f34514044877a8507c22c1bd85/interval_bound_propagation/src/utils.py#L84
    def smooth_schedule(self, step, init_step, final_step, init_value, final_value, mid_point=.25, beta=4.):
        """Smooth schedule that slowly morphs into a linear schedule."""
        assert final_value >= init_value
        assert final_step >= init_step
        assert beta >= 2.
        assert mid_point >= 0. and mid_point <= 1.
        mid_step = int((final_step - init_step) * mid_point) + init_step
        if mid_step <= init_step:
            alpha = 1.
        else:
            t = (mid_step - init_step) ** (beta - 1.)
            alpha = (final_value - init_value) / ((final_step - mid_step) * beta * t + (mid_step - init_step) * t)
        mid_value = alpha * (mid_step - init_step) ** beta + init_value
        is_ramp = float(step > init_step)
        is_linear = float(step >= mid_step)
        return (is_ramp * (
            (1. - is_linear) * (
                init_value +
                alpha * float(step - init_step) ** beta) +
            is_linear * self.linear_schedule(
                step, mid_step, final_step, mid_value, final_value)) +
                (1. - is_ramp) * init_value)

    # Linear schedule.
    # Code is adapted from DeepMind's IBP implementation:
    # https://github.com/deepmind/interval-bound-propagation/blob/2c1a56cb0497d6f34514044877a8507c22c1bd85/interval_bound_propagation/src/utils.py#L73
    def linear_schedule(self, step, init_step, final_step, init_value, final_value):
        """Linear schedule."""
        assert final_step >= init_step
        if init_step == final_step:
            return final_value
        rate = float(step - init_step) / float(final_step - init_step)
        linear_value = rate * (final_value - init_value) + init_value
        return np.clip(linear_value, min(init_value, final_value), max(init_value, final_value))


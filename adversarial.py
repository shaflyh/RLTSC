import torch
import numpy as np

def fgsm_attack(agent, obs, epsilon):
    # 'agent' is an instance of IDDQN which has sub-agents for each traffic signal
    # 'obs' is a dictionary with traffic signal IDs as keys and observation arrays as values
    
    # Dictionary to hold the perturbed observations
    perturbed_obs = {}

    # Loop through each traffic signal's observation and agent
    for ts_id, observation in obs.items():
        # Get the corresponding DQN agent for the current traffic signal
        dqn_agent = agent.agents[ts_id]

        # Convert observation to a PyTorch tensor and add batch dimension
        obs_tensor = torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
        obs_tensor = obs_tensor.to('cuda')
        obs_tensor.requires_grad = True
        
        # Get the current model prediction
        current_pred = dqn_agent.model(obs_tensor)
        
        # Access the 'q_values' directly for calculating the loss
        if hasattr(current_pred, 'q_values'):
            q_values = current_pred.q_values
            # Calculate the loss using the maximum value of the Q-values
            loss = -q_values.max()  # Assuming you want to minimize the maximum Q-value (inverting it here)
        else:
            raise ValueError("The model's output doesn't contain 'q_values'.")
        
        # Backpropagate to compute gradients with respect to the input observation
        loss.backward()
        
        # Create the perturbation using the sign of the gradients and multiply by epsilon
        perturbation = epsilon * obs_tensor.grad.sign()
        # print(perturbation)
    
        # Apply the perturbation and remove batch dimension
        perturbed_obs_tensor = (obs_tensor + perturbation).squeeze(0)
        
        # Detach and move back to CPU if necessary, then store in the dictionary
        perturbed_obs[ts_id] = perturbed_obs_tensor.detach().cpu().numpy()
        
        # print(obs_tensor)
        # print(perturbed_obs_tensor)
        # dsfdf

    return perturbed_obs


def pgd_attack(agent, obs, epsilon, num_iter=10):
    """
    Performs the PGD attack on an agent given the original observations.

    :param agent: The agent to attack, which contains DQN agents for each traffic signal.
    :param obs: The original observations, a dictionary with traffic signal IDs as keys.
    :param epsilon: The maximum magnitude of the allowable perturbation (L-infinity norm).
    :param alpha: The step size for each iteration of the attack.
    :param num_iter: The number of iterations to perform the attack.
    :return: A dictionary containing the perturbed observations.
    """
    # print('obs')
    # print(obs)
    
    alpha = epsilon / 10
    
    perturbed_obs = {}

    for ts_id, observation in obs.items():
        # Get the corresponding DQN agent for the current traffic signal
        dqn_agent = agent.agents[ts_id]

        # Convert observation to a PyTorch tensor and add batch dimension, moving it to GPU
        obs_tensor = torch.tensor(observation, dtype=torch.float32).unsqueeze(0).to('cuda')
        obs_tensor.requires_grad = False

        # Initialize perturbed observation with a small perturbation
        perturbed_obs_tensor = obs_tensor + 0.001 * torch.randn_like(obs_tensor).to('cuda')
        perturbed_obs_tensor = torch.clamp(perturbed_obs_tensor, 0, 1)  # Assuming obs values are in [0,1]
        perturbed_obs_tensor.requires_grad = True

        for _ in range(num_iter):
            # Compute the loss on the perturbed observation
            current_pred = dqn_agent.model(perturbed_obs_tensor)
            if hasattr(current_pred, 'q_values'):
                q_values = current_pred.q_values
                loss = -q_values.max()
            else:
                raise ValueError("The model's output doesn't contain 'q_values'.")

            # Backpropagate the error
            dqn_agent.model.zero_grad()
            loss.backward()

            # Perform the perturbation step and clip the result
            with torch.no_grad():
                perturbation = alpha * perturbed_obs_tensor.grad.sign()
                perturbed_obs_tensor += perturbation
                perturbed_obs_tensor = torch.clamp(perturbed_obs_tensor, obs_tensor - epsilon, obs_tensor + epsilon)
                perturbed_obs_tensor = torch.clamp(perturbed_obs_tensor, 0, 1)  # Ensure perturbed_obs stays within valid range
                perturbed_obs_tensor.requires_grad = True

        # Detach the final version of perturbed_obs_tensor and move to CPU
        perturbed_obs[ts_id] = perturbed_obs_tensor.detach().squeeze(0).cpu().numpy()
        
    # print('perturbed_obs')
    # print(perturbed_obs)

    return perturbed_obs
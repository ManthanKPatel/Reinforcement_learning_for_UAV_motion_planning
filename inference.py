from cgi import test
import os
import gym
import yaml
import pickle
import torch

from stable_baselines3 import PPO, DQN, DDPG, A2C
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecTransposeImage
from scripts.network import NatureCNN
from scripts.network import BasicCNN, AdvCNN
import airsim


# Load train environment configs
with open('scripts/env_config.yml', 'r') as f:
    env_config = yaml.safe_load(f)

# Load inference configs
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# Model name
# model_name = "best_model_" + config["test_mode"]
model_name = "best_model"

# Determine input image shape
image_shape = (50,50,1) if config["test_mode"]=="depth" else (50,50,3)

# Create a DummyVecEnv
env = DummyVecEnv([lambda: Monitor(
    gym.make(
        "scripts:test-env-v0", 
        ip_address="10.0.0.167", 
        image_shape=image_shape,
        # Train and test envs shares same config for the test
        env_config=env_config["TrainEnv"],          
        input_mode=config["test_mode"],
        test_mode=config["test_type"]
    )
)])

# Wrap env as VecTransposeImage (Channel last to channel first)
env = VecTransposeImage(env)

# policy_kwargs = dict(features_extractor_class=BasicCNN, optimizer_class= torch.optim.RMSprop, optimizer_kwargs= {'alpha': 0.99, 'eps': 1e-05, 'weight_decay': 0})
policy_kwargs = dict(features_extractor_class=BasicCNN)

# Load an existing model
model = PPO.load(
    env=env,
    path=os.path.join("saved_policy", model_name),
    policy_kwargs=policy_kwargs
)

# model = DDPG.load(
#     env=env,
#     path=os.path.join("saved_policy", model_name),
#     policy_kwargs=policy_kwargs
# )

# Run the trained policy
obs = env.reset()
pose = [[0, 0, 0]]
result_dict = {}
for i in range(1000):
    #print(i)
    action, _ = model.predict(obs, deterministic=True)
    obs, _ , dones, info= env.step(action)
#     x, y, z = airsim.MultirotorClient(ip="10.0.0.167").simGetVehiclePose().position
#     # print(obs)
#     pose.append([x, y, z])
#     if dones:
#         result_dict['Path'] = pose
#         # result_dict['distance'] = dist
#         break

# # save dictionary to person_data.pkl file
# print("dict:", result_dict)
# with open('result_data.pkl', 'wb') as fp:
#     pickle.dump(result_dict, fp)
#     print('dictionary saved successfully to file')


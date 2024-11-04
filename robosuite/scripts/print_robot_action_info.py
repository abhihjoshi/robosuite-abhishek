import argparse
import json

import robosuite as suite
from robosuite.controllers import load_composite_controller_config

parser = argparse.ArgumentParser()

parser.add_argument("--environment", type=str, default="Lift")
parser.add_argument("--robots", nargs="+", type=str, default="Panda", help="Which robot(s) to use in the env")
parser.add_argument("--config", type=str, default="opposed", help="Specified environment configuration if necessary")
parser.add_argument(
    "--controller",
    type=str,
    default=None,
    help="Choice of controller. Can be generic (eg. 'BASIC' or 'WHOLE_BODY_IK') or json file (see robosuite/controllers/config for examples)",
)

args = parser.parse_args()

controller_config = load_composite_controller_config(
    controller=args.controller,
    robot=args.robots[0],
)

config = {
    "env_name": args.environment,
    "robots": args.robots,
    "controller_configs": controller_config,
}

# Check if we're using a multi-armed environment and use env_configuration argument if so
if "TwoArm" in args.environment:
    config["env_configuration"] = args.config

# Create environment
env = suite.make(
    **config,
    has_renderer=True,
    ignore_done=True,
    use_camera_obs=False,
    reward_shaping=True,
    control_freq=20,
)
env.reset()

print(f"Action info for {args.environment}")
for robot in env.robots:
    print(f"Action info for {robot.name}")
    print(json.dumps(robot._action_split_indexes, indent=4))
    print()


env.close()

print(
    "Actions can created by calling robot.create_action_vector, and passing in a dictionary with the above keys and desired values."
)
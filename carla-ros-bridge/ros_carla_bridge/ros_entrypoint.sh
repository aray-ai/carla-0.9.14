#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /root/carla-ros-bridge/install/setup.bash

exec "$@"

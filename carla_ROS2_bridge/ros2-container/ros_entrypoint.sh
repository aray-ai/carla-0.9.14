#!/bin/bash
set -e

mkdir -p /tmp/runtime-root
source /opt/ros/humble/setup.bash
source /opt/carla-ros-bridge/install/setup.bash

exec "$@"

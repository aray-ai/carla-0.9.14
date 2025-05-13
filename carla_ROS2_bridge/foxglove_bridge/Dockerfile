# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

# ROS2 Humble is used for the ros carla bridge.

#FROM  osrf/ros:humble-desktop AS base

#RUN apt update && apt install -y ros-humble-foxglove-bridge

FROM osrf/ros:humble-desktop

# Install foxglove_bridge and other dependencies
RUN apt update && apt install -y \
    ros-humble-foxglove-bridge \
    python3-colcon-common-extensions \
    ros-humble-rosbridge-server \
    wget \
    git \
    && apt clean

# Set environment for ROS
ENV ROS_DOMAIN_ID=0
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# Source ROS 2 setup on shell start
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Copy launch file into container
COPY foxglove_bridge_launch.xml /launch/foxglove_bridge_launch.xml

# Set default workdir and source environment
WORKDIR /launch


# Default command to launch foxglove_bridge
CMD ["ros2", "launch", "foxglove_bridge", "foxglove_bridge_launch.xml", "port:=8765"]

# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

# ROS2 Humble is used for the ros carla bridge.

#FROM  osrf/ros:humble-desktop AS base

#RUN apt update && apt install -y ros-humble-foxglove-bridge

FROM osrf/ros:humble-desktop

# Install system dependencies and ROS packages
RUN apt update && apt install -y \
    ros-humble-foxglove-bridge \
    python3-colcon-common-extensions \
    git \
    wget \
    && apt clean

# Set environment variables
ENV ROS_DOMAIN_ID=0
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ENV ROS_WS=/opt/ros_ws

# Create workspace directory
RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS

# Clone only the carla_msgs package from the official standalone repo
RUN git clone https://github.com/carla-simulator/ros-carla-msgs.git src/carla_msgs

# Source ROS 2 setup, install dependencies, and build the carla_msgs package
RUN . /opt/ros/humble/setup.sh && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    colcon build --packages-select carla_msgs

# Source workspaces for container shell sessions
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source $ROS_WS/install/setup.bash" >> ~/.bashrc

# Copy custom launch file and entrypoint script
COPY foxglove_bridge_launch.xml /launch/foxglove_bridge_launch.xml
COPY fox_entrypoint.sh /fox_entrypoint.sh
RUN chmod +x /fox_entrypoint.sh

# Use entrypoint to source environments
ENTRYPOINT ["/fox_entrypoint.sh"]

# Default command: launch foxglove_bridge on port 8765
CMD ["ros2", "launch", "foxglove_bridge", "/launch/foxglove_bridge_launch.xml", "port:=8765"]

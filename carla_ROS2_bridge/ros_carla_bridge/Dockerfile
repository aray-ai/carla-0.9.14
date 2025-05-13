# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

#FROM ros2-humble-full:latest
FROM  osrf/ros:humble-desktop AS base

SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN apt update && apt install -y wget 

# installing the git
RUN apt update && apt install -y git

# Install required ROS message package
RUN apt update && \
    apt install -y ros-humble-derived-object-msgs python3-colcon-common-extensions
#    ros-humble-derived-object-msgs

# Install pip
RUN apt update && apt install -y python3-pip
    
# Install Python dependencies
RUN pip3 install pygame transforms3d

# Create workspace
ENV ROS_WS=/root/carla-ros-bridge
RUN mkdir -p ${ROS_WS}/src
WORKDIR ${ROS_WS}/src

# Clone Carla ROS bridge (gezp's repo for CARLA 0.9.14)
RUN git clone --recurse-submodules https://github.com/gezp/carla_ros.git -b humble-carla-0.9.14

# Install ROS dependencies
WORKDIR ${ROS_WS}
RUN source /opt/ros/humble/setup.bash && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y && \
    colcon build --symlink-install

# Source environment in container shell
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source ${ROS_WS}/install/setup.bash" >> ~/.bashrc
    
# Copy and install carla egg
RUN wget https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/carla-egg-whl/carla-0.9.14-cp310-cp310-linux_x86_64.whl -O /root/carla-0.9.14-cp310-cp310-linux_x86_64.whl && \
    pip3 install /root/carla-0.9.14-cp310-cp310-linux_x86_64.whl

RUN python3 -m pip install --upgrade pip && python3 -m pip install numpy pygame carla

# Add entrypoint
COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]

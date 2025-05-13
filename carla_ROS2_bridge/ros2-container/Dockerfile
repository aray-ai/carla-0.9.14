# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

FROM osrf/ros:humble-desktop

# Install colcon
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Setup ROS 2 Workspace
SHELL ["/bin/bash", "-c"]

# Copy your workspace
COPY ./ros2_ws /ros2_ws
WORKDIR /ros2_ws

# Build the workspace
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install
    

SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN apt update && apt install -y wget 

# installing the git
RUN apt update && apt install -y git

# Install pip
RUN apt update && apt install -y python3-pip
    
# Install Python dependencies
RUN pip3 install pygame transforms3d
    
# Copy and install carla egg
RUN wget https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/carla-egg-whl/carla-0.9.14-cp310-cp310-linux_x86_64.whl -O /root/carla-0.9.14-cp310-cp310-linux_x86_64.whl && \
    pip3 install /root/carla-0.9.14-cp310-cp310-linux_x86_64.whl
    
COPY ./ros_entrypoint.sh /

# Ensure script is executable
RUN ["chmod", "+x", "/ros_entrypoint.sh"]

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

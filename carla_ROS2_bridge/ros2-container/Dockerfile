# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14


FROM carlasim/carla:0.9.14 AS carla

FROM ros:humble-ros-base

# Install dependencies
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    python3-pip \
    git \
    wget \
    curl \
    ros-humble-rviz2 \
    ros-humble-rviz-common \
    ros-humble-rviz-default-plugins \
    ros-humble-pcl-conversions \
    ros-humble-pcl-ros \
    ros-humble-tf2 \
    ros-humble-tf2-eigen \
    ros-humble-tf2-ros \
    ros-humble-sensor-msgs \
    libtf2-eigen-dev

# Fix pip issue
RUN pip install setuptools==65.5.1

# Install Python dependencies
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Set up colcon workspace
WORKDIR /opt/carla-ros-bridge
COPY ./src ./src

# Install CARLA PythonAPI
COPY --from=carla /home/carla/PythonAPI /opt/carla/PythonAPI

# Build ROS 2 workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# Source workspace in bashrc
RUN echo "source /opt/carla-ros-bridge/install/setup.bash" >> ~/.bashrc

# supress the audio warning from pygame
ENV SDL_AUDIODRIVER=dummy

# Entrypoint
COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]

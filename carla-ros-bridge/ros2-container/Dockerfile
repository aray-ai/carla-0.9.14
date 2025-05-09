# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# 1. This installtion uses Python 3.10. The link for egg file for Python 3.10 is given under the link.

# Download and install CARLA .whl file
#RUN wget https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/Egg-Whl-Files/carla-0.9.14-cp310-cp310-linux_x86_64.whl \
#    -O carla-0.9.14-cp310-cp310-linux_x86_64.whl && \
#    pip install ./carla-0.9.14-cp310-cp310-linux_x86_64.whl

# Optionally download .egg file if you want to add it to PYTHONPATH
#RUN wget https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/Egg-Whl-Files/carla-0.9.14-py3.10-linux-x86_64.egg \
#    -O /usr/src/app/carla-0.9.14-py3.10-linux-x86_64.egg

# 2. Locale setup
RUN apt update && \
    apt install -y locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# 3. Basic utilities and repo tools
RUN apt install -y software-properties-common curl gnupg2 lsb-release

# 4. Add ROS 2 repository
RUN add-apt-repository universe && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2.list

# 5. Update system packages (udev, systemd) and install ROS 2
RUN apt-get update && \
    apt-get install --only-upgrade -y udev systemd && \
    apt-get install -y ros-humble-desktop-full python3-rosdep python3-pip

# 6. rosdep initialization
RUN rosdep init && rosdep update

# 7. Create workspace
ENV ROS_WS=/opt/ros2_ws
RUN mkdir -p $ROS_WS/src
WORKDIR $ROS_WS

# 8. (Optional) Place any repo clone or .repos file here
# Example placeholder
# RUN git clone https://github.com/your_repo.git src/your_package

# 9. Install workspace dependencies (will fail if src is empty)
RUN rosdep install --from-paths src -y --ignore-src || echo "rosdep skipped - no packages in src"

# 10. Source ROS setup by default
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source $ROS_WS/install/setup.bash" >> ~/.bashrc

COPY ./ros_entrypoint.sh /

# 11. Ensure script is executable
RUN ["chmod", "+x", "/ros_entrypoint.sh"]

ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]

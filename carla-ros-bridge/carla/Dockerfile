# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

FROM ubuntu:20.04

# Non-interactive frontend
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies and add deadsnakes PPA
RUN apt-get update && \
    apt-get install -y software-properties-common curl wget unzip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-distutils && \
    apt-get clean

# Set python alternatives
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
 && update-alternatives --set python3 /usr/bin/python3.10

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Install additional CARLA dependencies
RUN apt-get update && apt-get install -y \
    libomp5 \
    libpng16-16 \
    libtiff5 \
    libjpeg8 \
    libgl1 \
    libglu1-mesa \
    libxext6 \
    libx11-6 \
    libxxf86vm1 \
    libsm6 \
    libice6 \
    libglib2.0-0 \
    libfreetype6 \
    libxrender1 \
    libzmq3-dev \
    && rm -rf /var/lib/apt/lists/*


# Download and extract CARLA 9.14
RUN mkdir -p /opt/carla
WORKDIR /opt/carla
    wget --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 10 https://github.com/carla-simulator/carla/releases/download/0.9.14/CARLA_0.9.14.tar.gz && \
    tar -xvzf CARLA_0.9.14.tar.gz && \
    rm CARLA_0.9.14.tar.gz


# If above download does not work..
# Download the file manually and keep in the same loaction of this Dockerfile    
#COPY CARLA_0.9.14.tar.gz /opt/carla/
#RUN tar -xvzf /opt/carla/CARLA_0.9.14.tar.gz -C /opt/carla && \
#    rm /opt/carla/CARLA_0.9.14.tar.gz

# Download Python 3.10 compatible CARLA PythonAPI files

# Copy and install carla egg
# Download CARLA .whl file from github.

WORKDIR /opt/carla/PythonAPI/carla/dist

RUN wget --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 10 https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/Egg-Whl-Files/carla-0.9.14-cp310-cp310-linux_x86_64.whl && \
    wget --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 10 https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/Egg-Whl-Files/carla-0.9.14-py3.10-linux-x86_64.egg

# Download these below file manually and keep in the same loaction of this Dockerfile
# The below 2 lines can be commented, if you use the above github link to download the *.whl file.
#COPY carla-0.9.14-cp310-cp310-linux_x86_64.whl /opt/carla/PythonAPI/carla/dist/
#COPY carla-0.9.14-py3.10-linux-x86_64.egg /opt/carla/PythonAPI/carla/dist/

# Install CARLA PythonAPI
RUN python3 -m pip install carla-0.9.14-cp310-cp310-linux_x86_64.whl

# Set environment variables
ENV PYTHONPATH=/opt/carla/PythonAPI/carla/dist/carla-0.9.14-py3.10-linux-x86_64.egg:$PYTHONPATH

# Create non-root user and switch to it
RUN useradd -ms /bin/bash carla
USER carla

# Set working directory
WORKDIR /opt/carla


# Command to run CARLA
CMD ["/opt/carla/CarlaUE4.sh"]



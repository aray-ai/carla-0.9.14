# https://arayinfosolutions.com/
# This is the ros2 carla9.14 integration.
# Related files can be found under our aray-ai github repository.
# https://github.com/aray-ai/carla-0.9.14

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.10 from Deadsnakes
RUN apt-get update && \
    apt-get install -y software-properties-common wget curl && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-distutils && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Set python3 default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install required system libraries
RUN apt-get update && apt-get install -y \
    libjpeg8 \
    libtiff5 \
    libpng16-16 \
    libgl1 \
    libglu1-mesa \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy your app code
COPY . .

# Install Python dependencies
RUN pip install --upgrade --ignore-installed -r requirements.txt

# Install CARLA Python API wheel
RUN wget https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/Egg-Whl-Files/carla-0.9.14-cp310-cp310-linux_x86_64.whl -O carla-0.9.14-cp310-cp310-linux_x86_64.whl && \
    pip install ./carla-0.9.14-cp310-cp310-linux_x86_64.whl

# (Optional) Download .egg if you use PYTHONPATH manually — likely not needed
# RUN wget https://raw.githubusercontent.com/aray-ai/carla-0.9.14/main/Egg-Whl-Files/carla-0.9.14-py3.10-linux-x86_64.egg -O /PythonAPI/carla/dist/carla-0.9.14.egg

# Use client.py when you want to test the automated script.
#CMD ["python3", "./client.py"]  
CMD ["bash"]

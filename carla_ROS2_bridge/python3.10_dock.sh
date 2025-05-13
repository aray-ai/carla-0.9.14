#!/bin/bash

# Exit on any error
set -e

echo ">>> Installing dependencies..."
apt-get update && apt-get install -y \
    wget build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev \
    libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev

PYTHON_VERSION=3.10.14
PYTHON_SRC_DIR=/usr/src/python

echo ">>> Downloading Python $PYTHON_VERSION source..."
mkdir -p $PYTHON_SRC_DIR
cd $PYTHON_SRC_DIR
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz

echo ">>> Extracting..."
tar xvf Python-$PYTHON_VERSION.tgz
cd Python-$PYTHON_VERSION

echo ">>> Configuring and building Python..."
./configure --enable-optimizations
make -j$(nproc)

echo ">>> Installing Python $PYTHON_VERSION using altinstall..."
make altinstall

echo ">>> Verifying python3.10 and pip3.10 installation..."
python3.10 --version
python3.10 -m ensurepip --upgrade
python3.10 -m pip install --upgrade pip setuptools wheel

echo "✅ Python 3.10 and pip installed successfully!"

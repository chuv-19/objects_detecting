#!/bin/bash

# Create directories
mkdir -p objects_detecting
cd objects_detecting

# Clone the Git repository
git clone https://github.com/chuv-19/objects_detecting.git .
git pull origin master

# Install Python and required libraries
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install required libraries
pip3 install -r requirements.txt


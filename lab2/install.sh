#!/bin/bash

echo "Updating the package list..."
sudo apt-get update

echo "Checking and installing pip..."
sudo apt-get install -y python3-pip

echo "Installing Python libraries..."

# pandas
pip3 install pandas

# matplotlib
pip3 install matplotlib

# seaborn
pip3 install seaborn

# statsmodels
pip3 install statsmodels

echo "All libraries have been successfully installed."

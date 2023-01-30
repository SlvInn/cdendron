#!/bin/sh
# create_venv.sh

# to avoid connection errors:
export http_proxy=http://webproxy.science.gc.ca:8888/
export https_proxy=http://webproxy.science.gc.ca:8888/



echo " > creating a virtual environment 'venv'"
# # # # python3 -m venv ./venv 
# # virtualenv -p python3 ./venv
virtualenv --python="/usr/bin/python3" ./venv


# # activate the environment:
source ./venv/bin/activate
python3 -m pip install --upgrade pip


echo " > install the required packages in ./venv"
pip3 install -r requirements.txt 
# # # ifyou have problems with cartopy, try (uninstalling and re-)installing shapely using:
# pip uninstall shapely; pip install --no-binary :all: shapely


# # deactivate the environment:
deactivate
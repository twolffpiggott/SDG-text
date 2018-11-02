#!/bin/bash

# run this from your root directory

# install python3.7
# if your running ubuntu 16.04
# follow this link: https://medium.com/@manivannan_data/install-python3-7-in-ubuntu-16-04-dfd9b4f11e5c

# # Install requirements
# sudo apt-get install -y build-essential
# sudo apt-get install -y checkinstall
# sudo apt-get install -y libreadline-gplv2-dev
# sudo apt-get install -y libncursesw5-dev
# sudo apt-get install -y libssl-dev
# sudo apt-get install -y libsqlite3-dev
# sudo apt-get install -y tk-dev
# sudo apt-get install -y libgdbm-dev
# sudo apt-get install -y libc6-dev
# sudo apt-get install -y libbz2-dev
# sudo apt-get install -y zlib1g-dev
# sudo apt-get install -y openssl
# sudo apt-get install -y libffi-dev
# sudo apt-get install -y python3-dev
# sudo apt-get install -y python3-setuptools
# sudo apt-get install -y wget
# # Prepare to build
# mkdir /tmp/Python37
# cd /tmp/Python37
# # Pull down Python 3.7, build, and install
# wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
# tar xvf Python-3.7.0.tar.xz
# cd /tmp/Python37/Python-3.7.0
# ./configure --enable-optimizations
# sudo make altinstall

virtualenv --no-site-packages -p python3.7 sdg_env
source sdg_env/bin/activate
pip install -r setup/requirements.txt
python -m ipykernel install --user --name zindi_sdg

source sdg_env2/bin/activate
pip install -r setup/requirements2.txt
python -m ipykernel install --user --name zindi_sdg_tf

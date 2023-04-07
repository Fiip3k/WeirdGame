#!/usr/bin/env bash
# exit on error
set -o errexit


sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
$ sudo apt install python3.11

python -m pip install --upgrade pip
pip install -r requirements.txt
python mysite/manage.py collectstatic --no-input

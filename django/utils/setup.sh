#!/bin/bash

python3 -m venv django-env
source django-env/bin/activate


pip install --upgrade pip

pip install -r /requirements.txt


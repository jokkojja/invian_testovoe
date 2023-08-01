#!/bin/bash
python3 -m venv testovoe.env
source testovoe.env/bin/activate
pip install -r requirements.txt
git clone https://github.com/ultralytics/yolov5

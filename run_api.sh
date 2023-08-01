#!/bin/bash
git clone https://github.com/jokkojja/invian_testovoe.git
cd invian_testovoe
python3 -m venv testovoe.env
source testovoe.env/bin/activate
pip install -r requirements.txt
git clone https://github.com/ultralytics/yolov5

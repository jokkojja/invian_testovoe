# Fire detection API. 
## How to start
1. git clone https://github.com/jokkojja/invian_testovoe.git
2. cd invian_testovoe
3. Move .env into invian_testovoe
4. chmod +x prepare.sh
5. ./prepare.sh

## If windows
1. git clone https://github.com/jokkojja/invian_testovoe.git
2. cd invian_testovoe
3. Move .env into invian_testovoe
4. python3 -m venv testovoe.env
5. source testovoe.env/bin/activate
6. pip install -r requirements.txt
7. git clone https://github.com/ultralytics/yolov5

## All ready to use API
* to run all tests use command: python -m unittest discover -s tests

* to run API use command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
* documentation to the api is available at: http://0.0.0.0:8000/docs#/
# Fire detection API. How to start
1. git clone https://github.com/jokkojja/invian_testovoe.git
2. cd invian_testovoe
3. chmod +x run_api.sh
4. ./run_api.sh

## All ready to use API
* to run all tests use command: python -m unittest discover -s tests

* to run API use command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
* documentation to the api is available at: http://0.0.0.0:8000/docs#/
# invian_testovoe
1. git clone https://github.com/jokkojja/invian_testovoe.git
2. cd invian_testovoe
3. python3 -m venv testovoe.env
4. source testovoe.env/bin/activate
5. pip install -r requirements.txt

* to run all tests use command: python -m unittest discover -s tests
* to run API use command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
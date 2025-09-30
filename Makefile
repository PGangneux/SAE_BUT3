APP = API
manage = ./backend/manage.py
venv = venv/bin/python

.PHONY: run, install, migration, tests

run_back:
	$(venv) $(manage) runserver

run_front:
	npm --prefix ./frontend run dev

install:
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt

migration:
	$(venv) $(manage) makemigrations $(APP)
	$(venv) $(manage) migrate

tests:
	$(venv) $(manage) test $(APP)
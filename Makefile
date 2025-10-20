APP = API
manage = ./backend/manage.py
venv = venv/bin/python
pip = venv/bin/pip
npm = npm --prefix ./frontend

.PHONY: run, install, migration, tests

run_back:
	$(venv) $(manage) runserver

run_front:
	$(npm) run dev

install:
	python3 -m venv venv
	$(pip) install -r requirements.txt
	$(npm) install

migration:
	$(venv) $(manage) makemigrations $(APP)
	$(venv) $(manage) migrate

tests:
	$(venv) $(manage) test $(APP)
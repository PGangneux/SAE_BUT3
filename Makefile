APP = API
manage = ./backend/manage.py
venv = venv/bin/python

.PHONY: run install migration tests run_back shell run_front

run_back:
	$(venv) $(manage) runserver

shell:
	$(venv) $(manage) shell -v 2

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

neomodel_gen_diagram:
	venv/bin/neomodel_generate_diagram ./backend/API/models.py --file-type arrows --write-to-dir img

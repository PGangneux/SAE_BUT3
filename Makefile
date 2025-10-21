APP = API
manage = ./backend/manage.py
venv = venv/bin/python
pip = venv/bin/pip
npm = npm --prefix ./frontend

.PHONY: install migration tests run_back shell run_front neomodel_gen_diagram show_django_urls

run_back:
	$(venv) $(manage) runserver

shell:
	$(venv) $(manage) shell -v 2

run_front:
	$(npm) run dev

install:
	python3 -m venv venv
	$(pip) install -r requirements.txt
	$(npm) install

# Pour le backend
migration:
	$(venv) $(manage) makemigrations $(APP)
	$(venv) $(manage) migrate
	$(venv) $(manage) install_labels

tests:
	$(venv) $(manage) test $(APP)

neomodel_gen_diagram:
	venv/bin/neomodel_generate_diagram ./backend/API/models.py --file-type arrows --write-to-dir img

show_django_urls:
	$(venv) $(manage) show_urls

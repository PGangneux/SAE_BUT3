APP = API
manage = ./backend/manage.py
venv = venv/bin
python = ${venv}/python
pip = ${venv}/pip
npm = npm --prefix ./frontend

.PHONY: install migration tests run_back shell run_front neomodel_gen_diagram show_django_urls load_bd default_admin_user

run_back:
	$(python) $(manage) runserver

shell:
	$(python) $(manage) shell -v 2

run_front:
	$(npm) run dev

install:
	python3 -m venv venv
	$(pip) install -r requirements.txt
	$(npm) install

# Pour le backend
migration:
	$(python) $(manage) makemigrations $(APP)
	$(python) $(manage) migrate
	$(python) $(manage) install_labels

tests:
	$(python) $(manage) test $(APP)

neomodel_gen_diagram:
	${venv}/neomodel_generate_diagram ./backend/API/models.py --file-type arrows --write-to-dir img

load_bd:
	$(python) $(manage) install_labels
	$(python) $(manage) basic_load_bd

show_django_urls:
	$(python) $(manage) show_urls

default_admin_user:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=admin \
	$(python) $(manage) createsuperuser --noinput --email ""
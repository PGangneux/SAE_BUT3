APP = API
manage = ./backend/manage.py
venv = venv/bin
python = ${venv}/python
pip = ${venv}/pip
npm = npm --prefix ./frontend
coverage = $(venv)/coverage

.PHONY: install migration tests coverage run_back shell run_front neomodel_gen_diagram show_django_urls load_bd default_admin_user clean

run_back:
	$(python) $(manage) runserver

shell:
	$(python) $(manage) shell -v 2

run_front:
	$(npm) run dev

install:
	python3 -m venv venv
	$(pip) install -r backend/requirements.txt
	$(npm) install

# Pour le backend
migration:
	$(python) $(manage) makemigrations $(APP)
	$(python) $(manage) migrate
	$(python) $(manage) install_labels

# Nécessite d'avoir un serveur Neo4j sur les ports 17474 et 17687
# docker run -d -p 17474:7474 -p 17687:7687 -e NEO4J_AUTH=neo4j/testtest neo4j:latest
tests:
	$(python) $(manage) test $(APP)

coverage:
	$(coverage) run --source='$(APP)' $(manage) test ./backend/$(APP)/tests/$(package)
	$(coverage) report
	$(coverage) html

neomodel_gen_diagram:
	${venv}/neomodel_generate_diagram ./backend/API/models.py --file-type arrows --write-to-dir schema

load_bd:
	$(python) $(manage) install_labels
	$(python) $(manage) basic_load_bd

show_django_urls:
	$(python) $(manage) show_urls

default_admin_user:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=admin \
	$(python) $(manage) createsuperuser --noinput --email ""

clean:
	set -e
	@echo "python"
	@echo "rm -rv ./venv  || true"
	find ./backend/ -type d -name .mypy_cache | xargs rm -rv || true
	find ./backend/ -type d -name .pytest_cache | xargs rm -rv || true
	find ./backend/ -type d -name __pycache__ | xargs rm -rv || true
	find ./backend/ -type f -name "*.pyc" | xargs rm -rv || true
	@echo "vuejs"
	find ./frontend/ -type d -name node_modules | xargs rm -rv || true
	find ./frontend/ -type d -name dist | xargs rm -rv || true
	find ./frontend/ -type d -name .lock | xargs rm -rv || true
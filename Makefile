PROJECT=./example_project
MANAGE=python $(PROJECT)/manage.py

help:
	@echo "make commands:"
	@echo "  make help    - this help"
	@echo "  make clean   - remove temporary files in .gitignore"
	@echo "  make test    - run test suite"
	@echo "  make resetdb - drop and recreate the database"
	@echo "  make release - publish a new release"


clean:
	find -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	rm -rf MANIFEST
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info


test:
	ENVIRONMENT=test $(MANAGE) test wjordpress


resetdb:
	$(MANAGE) sqlclear wjordpress | $(MANAGE) dbshell
	$(MANAGE) syncdb --noinput


heroku_resetdb:
	heroku pg:reset database --confirm wjordpress
	heroku run python example_project/manage.py syncdb


# remember you need `pip install wheel`
release:
	python setup.py sdist bdist_wheel upload


.PHONY: help clean test resetdb release

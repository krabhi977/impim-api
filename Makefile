help:
	@echo '    setup ................... setup the current environment to run the project properly'
	@echo '    run  .................... run project'
	@echo '    test  ................... run tests'
	@echo '    clean  .................. remove build files (*.pyc, etc.)'
	@echo '    requirements ............ update project dependencies from requirements.txt and test_requirements.txt'
	@echo '    ci ...................... run CI build'
	@echo '    update_deps ............. update project dependencies in requirements.txt'

run:
	@honcho start -f Procfile.local

test:
	@nosetests tests/

clean:
	@find . -name "*.pyc" -delete

requirements:
	pip install -r test_requirements.txt
	pip install -r requirements.txt

setup: requirements
	@sh setup.sh

ci: requirements test

update_deps:
	@pip freeze --local | grep -v coverage | grep -v honcho | grep -v mock | grep -v nose | grep -v six > requirements.txt

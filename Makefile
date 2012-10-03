run:
	@honcho start -f Procfile.local

test:
	@nosetests tests/

clean:
	@find . -name "*.pyc" -delete

requirements:
	pip install -r test_requirements.txt
	pip install -r requirements.txt

ci: requirements test
	git checkout master
	git pull
	git push git@ngit.globoi.com:images-project/images-api.git master

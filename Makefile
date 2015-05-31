deploy:
	virtualenv venv
	make start

start:
	pip install -r requirements.txt
	make update

update:
	python manage.py syncdb
	python manage.py migrate

run:
	python manage.py runserver

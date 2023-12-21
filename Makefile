
.PHONY: fdx
fdx:
	git clean -fdX

.PHONY: clean
clean:
	make fdx

.PHONY: push
push:
	git add .
	git commit -m up
	git push

.PHONY: up
up:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py shell -c "from django.contrib.auth import get_user_model; \
		get_user_model().objects.filter(username='admin').exists() or \
		get_user_model().objects.create_superuser('admin', 'admin@admin.com', 'admin')"
	python manage.py runserver 2000

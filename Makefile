setup:
	cd code && uv sync

start-server:
	cd code && uv run python manage.py runserver 0.0.0.0:3000

build:
	./build.sh

install:
	cd code && uv sync

collectstatic:
	cd code && uv run python manage.py collectstatic --noinput

migrate:
	cd code && uv run python manage.py migrate

render-start:
	cd code && uv run gunicorn task_manager.wsgi

start:
	cd code && uv run python manage.py runserver
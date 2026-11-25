build:
	./build.sh

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

render-start:
	uv run gunicorn task_manager.wsgi

start-server:
	uv run python manage.py runserver 0.0.0.0:3000

start:
	uv run python manage.py runserver

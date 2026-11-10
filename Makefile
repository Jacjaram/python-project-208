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

start:
	uv run python manage.py runserver

CODE_DIR := $(if $(filter code,$(notdir $(CURDIR))),.,code)

setup:
	cd $(CODE_DIR) && uv sync

start-server:
	cd $(CODE_DIR) && uv run python manage.py runserver 0.0.0.0:3000

build:
	./build.sh

install:
	cd $(CODE_DIR) && uv sync

collectstatic:
	cd $(CODE_DIR) && uv run python manage.py collectstatic --noinput

migrate:
	cd $(CODE_DIR) && uv run python manage.py migrate

render-start:
	cd $(CODE_DIR) && uv run gunicorn task_manager.wsgi

start:
	cd $(CODE_DIR) && uv run python manage.py runserver

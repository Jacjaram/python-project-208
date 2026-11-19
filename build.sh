#!/usr/bin/env bash
# Descargamos uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Comandos que tu proyecto necesita para funcionar
make install && make collectstatic && make migrate
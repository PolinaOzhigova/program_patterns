#!/bin/bash

python -m venv .venv
. .venv/bin/activate

pip install typing-extensions --upgrade
pip install dict2xml
pip install connexion[flask]
pip install connexion[swagger-ui]
pip install connexion[uvicorn]
pip install flask-restplus
pip install flask
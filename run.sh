#!/usr/bin/env bash

# Please don't forget to define an ENVIRONMENT VAR with the ACCESS TOKEN:
# export ACCESS_TOKEN=<token>

pip install -r requirements.txt
FLASK_APP=tunnel-manager.py flask run --host 0.0.0.0 --port 8080
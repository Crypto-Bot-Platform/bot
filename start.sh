#!/bin/zsh
export KAFKA_HOST=10.0.0.124
export ELASTIC_HOST=10.0.0.124
export MONGODB_HOST=10.0.0.124
export SQLDB_HOST=10.0.0.124
export BOT_ID='test-bot-02'

export PYTHONPATH="${PYTHONPATH}:${PWD}/"
pip install -r requirements.txt

cd bots/random && python3.9 ../../common/main/__main__.py
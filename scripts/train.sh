#!/usr/bin/bash

cd /work
python3 -m pip install -r requirements.txt &&
for i in {1..2}; do
    python3 -m src/models/train.py
done &&
python3 -m mlflow ui --host 0.0.0.0
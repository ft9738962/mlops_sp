#!/usr/bin/bash

cd /work
pip3 install -r requirement.txt &&
for i in {1..5}; do
    python3 models/mf_train_examply.py
done &&
python mlflow ui
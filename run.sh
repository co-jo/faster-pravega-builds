#!/bin/bash

python3 run.py --command="$(cat cmd)" --retries=5 --memory=6

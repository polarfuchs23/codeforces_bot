#!/bin/bash

python -m pip install -r requirements.txt
touch dm_channels.json
touch subscription1.csv
touch subscription2.csv
touch subscription3.csv
touch subscription4.csv
read -p "Discord token: " TOKEN
touch .env
echo "TOKEN=$TOKEN">.env

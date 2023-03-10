#!/bin/bash

pip install -r requirements.txt
touch dm_channels.json
read -p "Discord token: " TOKEN
touch .env
cat "TOKEN=$TOKEN">.env

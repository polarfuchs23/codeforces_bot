pip install -r requirements.txt
touch dm_channels.json
read -p "Discord token: " TOKEN
cat "TOKEN=$TOKEN">.env
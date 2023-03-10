@echo off
pip install -r requirements.txt
echo pip installs done...
echo. {}>dm_channels.json
set /p TOKEN="Discord token: "
echo TOKEN=%TOKEN%>.env
pause
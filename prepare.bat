@echo off
pip install -r requirements.txt
echo pip installs done...
echo. {}>dm_channels.json
cd. >subscription1.csv
cd. >subscription2.csv
cd. >subscription3.csv
cd. >subscription4.csv
set /p TOKEN="Discord token: "
echo TOKEN=%TOKEN%>.env
pause

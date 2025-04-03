wget https://github.com/abhinavudupi/BhandariBox/archive/refs/heads/main.zip
mv BhandariBox-main/ ContribWebUI/
rm main.zip
cd ContribWebUI
chmod 777 run.sh
apt-get update
echo "execute 'sudo bash setup.sh <ssid> <key>' to setup application"

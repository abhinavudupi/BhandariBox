#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Enter SSID and Key for Access Point"
  exit 1
fi
if [ $# -eq 1 ]; then
  echo "Enter SSID and Key for Access Point"
  exit 1
fi

echo "System Update"
apt-get update

echo "currently in $(pwd)"
mv=$(pwd)
un=$(basename "$(dirname "$(dirname "$(pwd)")")")
printf "[APPLICATION]\nApplicationDirectory =" > app.conf
sed -i -r "s#^(ApplicationDirectory =).*#\1 $mv#" app.conf

echo "Installing dependencies"
cat requirements.txt | xargs sudo apt-get -y install
pip3 install -r pip_requirements.txt 

echo "Adding run.sh to rc.local"
#exec 1>/tmp/rc.local.log 2>&1
sed -i -e '$i \su -c '"'"''"$mv"'/run.sh &'"'"' '"$un"' ' /etc/rc.local

echo "execute 'sudo raspi-config' and disable screen blanking and enable auto login to desktop"
echo "Application has been setup and will start on reboot"

echo "Do you want to continuewith Access Point setup? (y/n)"
read -r answer

if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    echo "Continuing ..."
else
    echo "Exiting without accesspoint setup."
    exit 1
fi

echo "Setting up Access Point with SSID : $1 and Key : $2"
systemctl enable NetworkManager
service NetworkManager start
nmcli con add con-name bboxspot ifname wlan0 type wifi ssid "$1"
nmcli con modify bboxspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify bboxspot wifi-sec.key-mgmt wpa-psk
nmcli con modify bboxspot wifi-sec.psk "$2"
nmcli con up bboxspot

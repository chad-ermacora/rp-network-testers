#!/usr/bin/env bash
# HTTP Server Options
HTTP_SERVER="http://kootenay-networks.com"
HTTP_FOLDER="/utils/koot_net_eth_testers"
HTTP_ZIP="/KootNetEthTesters.zip"
# Other Option
APT_GET_INSTALL="fonts-freefont-ttf mtr iperf3 wget"
# Don't change INSTALL_DIR
INSTALL_DIR="/opt/kootnet-network-testers"
# Make sure its running with root
clear
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Install
mkdir ${INSTALL_DIR}  2>/dev/null
mkdir ${INSTALL_DIR}/backup  2>/dev/null
printf "\nConfiguring Network\n"
# Add and edit TCP/IP v4 Network + Wireless
if [[ -f ${INSTALL_DIR}/backup/interfaces ]]
then
  printf "\nPrevious install detected, restoring interfaces before install\n"
  cp -f ${INSTALL_DIR}/backup/interfaces /etc/network/interfaces 2>/dev/null
fi
cp -f /etc/network/interfaces ${INSTALL_DIR}/backup/ 2>/dev/null
cat >> /etc/network/interfaces << "EOF"

allow-hotplug eth0
iface eth0 inet static
    address 192.168.169.249
    netmask 255.255.255.0
EOF
printf "\n\nDownloads started\n"
wget ${HTTP_SERVER}${HTTP_FOLDER}${HTTP_ZIP} -P /tmp/
printf "Downloads complete\nUnzipping & installing files\n"
unzip /tmp/KootNetEthTesters.zip -d /tmp/KootNetEthTesters_files
cp -f -R /tmp/KootNetEthTesters_files/* ${INSTALL_DIR}
# Install needed programs and dependencies
printf '\nStarting system update & upgrade. This may take awhile ...\n\n'
apt-get update
apt-get -y upgrade
printf '\nChecking dependencies\n'
apt-get -y install ${APT_GET_INSTALL}
pip3 install pillow
printf "copying & enabling KootNet Ethernet Tester Display Services\n"
cp /opt/kootnet-network-testers/auto_start/KootnetEthServer.service /etc/systemd/system
systemctl daemon-reload
systemctl enable KootNetEthDisplay 2>/dev/null
printf "\nInstall Complete, Please Reboot\n"

#!/usr/bin/env bash
clear
if [[ "$1" == "dev" ]]
then
  HTTP_FOLDER="/utils/koot_net_eth_testers/dev"
  printf '\n-- DEVELOPMENT HTTP UPGRADE OR INSTALL --\n'
else
  printf '\n-- HTTP UPGRADE OR INSTALL --\n'
  HTTP_FOLDER="/utils/koot_net_eth_testers"
fi
if [[ "$2" == "skip" ]]
then
  SKIP="true"
else
  SKIP="false"
fi
# HTTP Server Options
HTTP_SERVER="http://kootenay-networks.com"
HTTP_ZIP="/KootNetEthTesters.zip"
# Other Option
APT_GET_INSTALL="wget mtr iperf3 fonts-freefont-ttf"
INSTALL_DIR="/opt/kootnet-network-testers"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Install
mkdir ${INSTALL_DIR} 2>/dev/null
mkdir ${INSTALL_DIR}/backup 2>/dev/null
rm /root/KootNetEthTesters.zip
printf "\nConfiguring Network\n"
# Add and edit TCP/IP v4 Network + Wireless
#if [[ -f ${INSTALL_DIR}/backup/interfaces ]]
#then
#  printf "\nPrevious install detected, restoring interfaces before install\n"
#  cp -f ${INSTALL_DIR}/backup/interfaces /etc/network/interfaces 2>/dev/null
#fi
#cp -f /etc/network/interfaces ${INSTALL_DIR}/backup/ 2>/dev/null
#cat >> /etc/network/interfaces << "EOF"
#
#allow-hotplug eth0
#iface eth0 inet static
#    address 192.168.169.251
#    netmask 255.255.255.0
#EOF
printf "\n\nDownloads started\n"
wget ${HTTP_SERVER}${HTTP_FOLDER}${HTTP_ZIP} -P /root/
printf "Downloads complete\nUnzipping & installing files\n"
rm -f -r /root/KootNetEthTesters_files
unzip -q /root/KootNetEthTesters.zip -d /root/KootNetEthTesters_files
cp -f -R /root/KootNetEthTesters_files/rp-network-testers/* ${INSTALL_DIR}
# Install needed programs and dependencies
if [[ ${SKIP} == "true" ]]; then
  printf '\nSkipping Dependincie Installs\n\n'
else
  printf '\nChecking dependencies\n\n'
  apt-get update
  apt-get -y install ${APT_GET_INSTALL}
  cd ${INSTALL_DIR} || exit
  python3 -m venv --system-site-packages python-env
  # shellcheck disable=SC1090
  source ${INSTALL_DIR}/python-env/bin/activate
  python3 -m pip install -U pip
  pip3 install -r ${INSTALL_DIR}/requirements.txt
  deactivate
fi
printf "copying & enabling KootNet Ethernet Tester Display Services\n"
cp ${INSTALL_DIR}/auto_start/KootnetEthServer.service /etc/systemd/system
systemctl daemon-reload
systemctl enable KootnetEthServer 2>/dev/null
systemctl start KootnetEthServer 2>/dev/null
printf "\nInstall Complete\n"
cd || exit

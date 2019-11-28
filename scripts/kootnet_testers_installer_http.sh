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
# HTTP Server Options
HTTP_SERVER="http://kootenay-networks.com"
HTTP_ZIP="/KootNetEthTesters.zip"
# Other Option
APT_GET_INSTALL="wget mtr iperf3 python3 python3-venv"
SECONDARY_APT_GET_INSTALL="fonts-freefont-ttf fake-hwclock"
INSTALL_DIR="/opt/kootnet-network-testers"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
# Start Install - Make sure directories are made
mkdir ${INSTALL_DIR} 2>/dev/null
mkdir ${INSTALL_DIR}/backup 2>/dev/null
# Remove Previous Downloads
rm /root${HTTP_ZIP}
rm -f -r /root/KootNetEthTesters_files
# Check for previous install
PREVIOUS_INSTALL="no"
if [[ -f ${INSTALL_DIR}/requirements.txt ]]
then
  PREVIOUS_INSTALL="yes"
fi
printf "\n\nDownloads started\n"
wget ${HTTP_SERVER}${HTTP_FOLDER}${HTTP_ZIP} -P /root/
printf "Downloads complete\nUnzipping & Installing Files\n"
unzip -q /root${HTTP_ZIP} -d /root/KootNetEthTesters_files
cp -f -R /root/KootNetEthTesters_files/rp-network-testers/* ${INSTALL_DIR}
# Install needed programs and dependencies
if [[ ${PREVIOUS_INSTALL} == "yes" ]]
then
  printf '\nSkipping Dependincie Installs\n\n'
else
  printf '\nChecking dependencies\n\n'
  apt-get update
  apt-get -y install ${APT_GET_INSTALL}
  apt-get -y install ${SECONDARY_APT_GET_INSTALL}
  cd ${INSTALL_DIR} || exit
  python3 -m venv --system-site-packages python-env
  # shellcheck disable=SC1090
  source ${INSTALL_DIR}/python-env/bin/activate
  python3 -m pip install -U pip
  pip3 install -r ${INSTALL_DIR}/requirements.txt
  deactivate
  cat > /usr/share/applications/KootNet-Network-Testers-Web.desktop << "EOF"
[Desktop Entry]
Name=Kootnet Network Testers
Comment=Web interface for running tests & configuring
Type=Application
Icon=/opt/kootnet-network-testers/operations_modules/extras/icon.png
TryExec=/usr/bin/x-www-browser
Exec=x-www-browser http://localhost:10066
Terminal=false
Categories=Utility;Science;
StartupNotify=true
EOF
fi
printf "copying & enabling KootNet Ethernet Tester Service\n"
cp ${INSTALL_DIR}/auto_start/KootnetEthServer.service /etc/systemd/system
systemctl daemon-reload
systemctl enable KootnetEthServer.service
systemctl restart KootnetEthServer.service
systemctl start KootnetEthServer.service
printf "\nInstall Complete\n"
cd || exit

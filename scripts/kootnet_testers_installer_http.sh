#!/bin/bash
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
clear
HTTP_SERVER="http://kootenay-networks.com"
HTTP_FOLDER="/installers"
DEB_INSTALLER="/KootnetNetworkTesters.deb"
INSTALL_TYPE="Standard"
# Check for development switch
if [[ "$1" == "dev" ]]; then
  HTTP_FOLDER="/installers/dev"
  INSTALL_TYPE="Developmental"
fi
printf '\n-- %s HTTP UPGRADE OR INSTALL --\n' "${INSTALL_TYPE}"
# Clean up previous downloads if any
rm -f /tmp${DEB_INSTALLER} 2>/dev/null
# Make sure apt-get is up-to-date (stale package lists can make upgrades and installs fail)
apt-get update
wget -O /tmp${DEB_INSTALLER} ${HTTP_SERVER}${HTTP_FOLDER}${DEB_INSTALLER}
apt-get -y install --reinstall /tmp${DEB_INSTALLER}

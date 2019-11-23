INSTALL_DIR="/opt/kootnet-network-testers"
SYSTEM_D_FILE="/etc/systemd/system/KootnetEthServer.service"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
printf "Uninstall Started ... "
systemctl disable KootnetEthServer 2>/dev/null
systemctl stop KootnetEthServer 2>/dev/null
rm ${SYSTEM_D_FILE} 2>/dev/null
rm -f -r ${INSTALL_DIR} 2>/dev/null
rm /usr/share/applications/KootNet-Network-Testers-Web.desktop
printf "Uninstall Complete\n"

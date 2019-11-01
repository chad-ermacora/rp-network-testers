INSTALL_DIR="/opt/kootnet-network-testers"
SYSTEM_D_FILE="/etc/systemd/system/KootnetEthServer.service"
# Make sure its running with root
if [[ $EUID != 0 ]]; then
  printf "\nStarting with sudo\n"
  sudo "$0" "$@"
  exit $?
fi
rm ${SYSTEM_D_FILE}
rm -f -r ${INSTALL_DIR}
printf "\n\nUninstall Complete\n"

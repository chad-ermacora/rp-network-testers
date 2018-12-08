# KootNet Ethernet Testers
These Python 3 programs turn 2x Raspberry Pis into Cat5/6 Network Testers. 
Use it to test individual cables or network routes on the same LAN.
[MTR](https://www.bitwizard.nl/mtr/) & [iPerf3](https://iperf.fr/) are used to test latency and throughput.

_Note: throughput is limited to the RP3B+'s 300Mbps network adapter_

Install & Setup
====================
Get a fresh copy of Raspbian running on both the Raspberry Pis.  
The display Pi requires a
[Waveshare e-Paper 2.7" Raspberry HAT](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT) (Black & White version)
to be installed before proceeding with installation. There is no special hardware required for the Server Pi.
Once the instructions are followed bellow and the devices rebooted, a message will display on the display Pi
 letting you know its ready to operate.

E-Ink display Pi - Install Command
---------------------
Be sure to enable SPI on the Pi first, then run the following command in a terminal window.

```wget http://kootenay-networks.com/utils/koot_net_eth_testers/display_pi_installer.sh && chmod +x display_pi_installer.sh && sudo bash display_pi_installer.sh && sudo reboot```

 Server Pi - Install Command
---------------------
Run the following command in a terminal window.

```wget http://kootenay-networks.com/utils/koot_net_eth_testers/server_installer.sh && chmod +x server_installer.sh && sudo bash server_installer.sh && sudo reboot```

Using KootNet Ethernet Testers
====================
Connect the 2 Pi's to a cable or local network then press the appropriate buttons to operate.  

_Note: Hold the buttons down for 1 second before releasing_

The 4 buttons are as follows.
1. Run & Display [MTR](https://www.bitwizard.nl/mtr/) tests
2. Run & Display [iPerf3](https://iperf.fr/) tests
3. Shutdown Remote "Server" Unit
4. Shutdown Local "Display" Unit

# KootNet Ethernet Testers
This Python 3 program turn 2x Linux Computers (Primarily Raspberry Pis) into Cat5/6 Network Testers. 
Use it to test individual cables or network routes on the same LAN.
[MTR](https://www.bitwizard.nl/mtr/) & [iPerf3](https://iperf.fr/) are used to test latency and throughput.

_Note: Throughput is limited to the Computers Network Adapter._  
_Raspberry Pi 3B+ = 300Mbps || Raspberry Pi 4B = 1000Mbps_

Install & Setup
====================
This has been tested on Raspbian Buster & Ubuntu but in theory should work on other Linux distributions.

You do not need any special hardware when used only through the web interface but it does support the following additional Displays and Interactive Hardware when installed on a Raspberry Pi.

[Waveshare e-Paper 2.7" Raspberry HAT](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT) (Any version)

1. Get a fresh copy of Raspbian running on both the Raspberry Pis.
2. Optional: Enable any requirements for special hardware (Such as SPI, IC2, etc.  Driver are included in the program)
3. Run the following command in a Terminal - Raspberry Pi 4B Recommended

```wget http://kootenay-networks.com/utils/koot_net_eth_testers/kootnet_testers_installer_http.sh && sudo bash kootnet_testers_installer_http.sh```

4. Goto http://localhost:10066 on the local unit to use and configure the Tester.  
You can also connect the tester to a wifi network and access the configuration page from another computer on the same network through http://IP-Address:10066

_Note: Remember to install this on 2 devices, one for interacting with and the other as the remote test server. 
You will need to set one of the testers as the remote test server in the configuration options._ 

Using KootNet Ethernet Testers
====================
Connect the 2 Pi's to a cable or local network then press the appropriate buttons or initiate tests over the web interface to operate.  

_Note: Hold the buttons down for 1 second before releasing_

The 4 buttons are as follows.
1. Run & Display [MTR](https://www.bitwizard.nl/mtr/) tests
2. Run & Display [iPerf3](https://iperf.fr/) tests
3. Shutdown Remote "Server" Unit
4. Shutdown Local "Display" Unit

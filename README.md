# KootNet Network Testers
This Python 3 program turn 2x Linux Computers (Primarily Raspberry Pis) into Network Testers by running 
[MTR](https://www.bitwizard.nl/mtr/) & [iPerf3](https://iperf.fr/) 
to test latency & throughput on individual cables or network routes.
No special hardware is required to use Kootnet Network Testers.  
_IPv4 support only.  IPv6 support coming soon._

_Note: Throughput is limited to the Networks Capacity and the Computers Network Adapter. The results will reflect the slowest link.  
Raspberry Pi 3B+ = 300Mbps || Raspberry Pi 4B = 1000Mbps_

Install & Setup
====================
_Raspberry Pi 4B Recommended due to it's 1GB network adapter_
####Supported & Tested Operating Systems
Raspbian (9 or higher), Ubuntu (18.04 or higher)
####Unsupported Operating Systems that will probably work
Most other GNU/Linux distributions that support MTR, iPerf3 & wget, along with Python3 and the Flask, gevent & requests modules.
If the OS supports those programs and modules, the install script will automatically download and install them from the internet.

###Optional Hardware
When installed on a Raspberry Pi you can install additional hardware such as displays and buttons to operate the unit.  
See below for supported optional hardware and it's operation.  

[Waveshare e-Paper 2.7" Raspberry Pi HAT](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT) (Both BW & BWR versions)  
_Note: This hardware uses the SPI Interface: Enable SPI in the RPi Configuration program_  
_Note: Hold the buttons down for 1 second before releasing to ensure proper operation._

###Installing Kootnet Network Testers
1. If using Raspberry Pis, get a fresh copy of Raspbian running on both of them, otherwise skip to step 3.
2. Optional: Enable requirements for optional hardware support like displays and buttons (SPI, IC2, etc. found in the Raspberry Pi configuration utility)
3. Run the following command in a Terminal

```wget http://kootenay-networks.com/utils/koot_net_eth_testers/kootnet_testers_installer_http.sh && sudo bash kootnet_testers_installer_http.sh```

4. Open a web browser like Firefox or Chrome and goto http://localhost:10066 on the local unit to use and configure the Tester.
5. Optional: Connect the tester to a wifi network and access the configuration page from another computer on the same network through the IP address. Example: http://192.168.1.121:10066

_Note: Remember to install this on 2 devices, one for interacting with and the other as the remote test server.  
By default, each Kootnet Network Tester can be used as the remote test server (This can be turned off in the configuration).
Set the remote test server IP in the unit's configuration._ 

Using KootNet Network Testers
====================
Connect the 2 Tester units to a single cable or local network then use the web interface or press the appropriate buttons to initiate tests.  

_Note: In order to use secondary button features on supported hardware, you must hit the same button twice in a row. 
Hitting any other button will reset the count._

The 4 buttons are as follows.
1. Run & Display [MTR](https://www.bitwizard.nl/mtr/) tests
2. Run & Display [iPerf3](https://iperf.fr/) tests
3. First Press: System Information || Second Press: Upgrade program over HTTP
4. Shutdown Local Unit

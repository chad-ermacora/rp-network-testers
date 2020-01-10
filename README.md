# KootNet Network Testers
This Python 3 program turn 2x Raspberry Pis (and some other GNU/Linux computers) into Network Testers by running 
[MTR](https://www.bitwizard.nl/mtr/) & [iPerf3](https://iperf.fr/) 
to test latency & throughput on individual cables or network routes.  
No special hardware is required to use Kootnet Network Testers.  
_IPv4 support only.  IPv6 support coming soon._

_Note: Throughput is limited to the Networks Capacity and the Computers Network Adapter.
The results will reflect the slowest link.  
Raspberry Pi 3B+ = 300Mbps || Raspberry Pi 4B = 1000Mbps_

Install & Setup
====================
_Raspberry Pi 4B Recommended due to it's 1000Mbps network adapter_  
#### Supported Operating Systems
Raspbian (9 or higher), Ubuntu (18.04 or higher)  
#### Other Operating Systems
Most other GNU/Linux distributions should work with Kootnet Network Testers if the distribution supports the applications
MTR, iPerf3, wget & Python3 along with the Flask & gevent Python modules.
The install script will automatically download the applications from your Operating System's repositories
and the Python modules with pip.

### Optional Hardware
When installed on a Raspberry Pi you can install additional hardware such as displays and buttons to operate the unit.  
See below for supported optional hardware and it's operation.  

[Waveshare e-Paper 2.7" Raspberry Pi HAT](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT) (Both BW & BWR versions)  
_Note: Hold the buttons down for 1 second before releasing to ensure proper operation._

### Installing Kootnet Network Testers
1. If using Raspberry Pis, ensure Raspbian is running on both of them, otherwise skip to step 2.  
Fresh Raspbian Installs Recommended [Download Raspbian Here](https://www.raspberrypi.org/downloads/)
2. Run the following command in a Terminal.

```wget http://kootenay-networks.com/utils/koot_net_eth_testers/kootnet_testers_installer_http.sh && sudo bash kootnet_testers_installer_http.sh```

3. Once the script has finished, open the "Kootnet Network Testers" shortcut in your Operating Systems application
menu to configure and use the Tester. On the Raspberry Pi, the shortcut is located in the Accessories menu.

Optional: If you cannot find the menu shortcut, you can open a web browser like Firefox or Chrome and goto
http://localhost:10066 on the local unit to use and configure the Tester.  
Optional: Connect the tester to a network and access the configuration page from another computer on the same network
through the IP address. Example: http://192.168.1.121:10066

_Note: You need to install Kootnet Network Testers on 2 devices to test throughput,
one for interacting with and the other as the remote test server.
By default, each Kootnet Network Tester can be used as the remote test server
(This can be turned off in the configuration).  
The remote test server IP can be found and set in the unit's configuration._ 

Using KootNet Network Testers
====================
If you intend to test cables or a network without a DHCP server,
be sure to set Static IP's in the testers configuration or the underlying Operating System.

You must set the "Remote Test Server IP" in the configuration of the tester you are intending to run tests from.  
Connect the 2 Tester units to a single cable or local network
then use the web interface or press the appropriate buttons to initiate tests.  

_Note: The "Change Button Functions" will cycle through 3 different settings when pressed multiple times._

### Primary Button Functions
1. Run & Display [MTR](https://www.bitwizard.nl/mtr/) tests
2. Run & Display [iPerf3](https://iperf.fr/) tests
3. Nothing (WIP)
4. Change Button Functions

### Secondary Button Functions
1. System Information
2. Upgrade Kootnet Ethernet Tester Software
3. Upgrade Kootnet Ethernet Tester Software Developmental
4. Change Button Functions

### Tertiary Button Functions
1. Shutdown Remote Test Server
2. Shutdown Local Unit
3. Nothing (WIP)
4. Change Button Functions

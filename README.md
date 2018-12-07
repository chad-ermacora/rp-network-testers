# Raspberry Pi Cat5/6 Network Testers
Python 3 application that turns 2x Raspberry Pi 3B+ into Ethernet Cable & Cable Run Testers

Once the instructions are followed bellow and the devices rebooted, they will automatically start the programs in about 15-25 seconds and be ready to use.

How to Use Devices
====================
After getting everything setup (see bellow), simply connect the 2 Pi's to a cable or local network then press the buttons to operate.  
* Note: The buttons have a bit of a delay, so hold it down for at least 1/2 a second before releasing

The 4 buttons are as follows.
1. Run MTR tests - www.bitwizard.nl/mtr/
2. Run iPerf3 tests - www.iperf.fr/iperf-doc.php
3. Shutdown Remote Unit
4. Shutdown Local Unit

How to Install 
====================
Get a fresh copy of Raspbian running on the two Raspberry Pi's then Update and install mtr/iperf3 on both systems 

```sudo apt-get update && sudo apt-get upgrade && sudo apt-get install mtr iperf3```

On the Raspberry Pi with E-Ink display
---------------------
Waveshare e-Paper 2.7" Raspberry HAT (Black & White version) - https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT

Files needed from repository
```
waveshare_library/epd2in7.py
waveshare_library/epdif.py
epsimplelib.py
network_display.py
```

Modify /etc/rc.local and Add the following between "fi" and "exit 0"
```
python3 /WHERE-EVER-YOU-PUT-IT/network_display.py &
```

Modify /etc/network/interfaces and add
```
iface eth0 inet static
    address 192.168.169.249
    netmask 255.255.255.0
```


Raspberry Pi running as the Server
---------------------
Files needed from repository
```
network_server.py
```

Modify /etc/rc.local and Add the following between "fi" and "exit 0"
```
iperf3 -s -p 9000 &
python3 /WHERE-EVER-YOU-PUT-IT/network_server.py &
```

Modify /etc/network/interfaces and add
```
iface eth0 inet static
    address 192.168.169.251
    netmask 255.255.255.0
```

# rp-network-testers
Python 3 application that turns 2x Raspberry Pi 3B+ into Ethernet Cable & Cable Run Testers

How to use
Get a fresh updated copy of Raspbian running on the two Raspberry Pi's
Run 'sudo apt-get install mtr iperf3' on both Raspberry Pi's

** Note: Don't add '' when following instructions **

On the Raspberry Pi with E-Ink display Waveshare e-Paper 2.7" Raspberry HAT (Black & White version)
  https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT

Files needed from repository
waveshare_library/epd2in7.py
waveshare_library/epdif.py
epsimplelib.py
network_display.py

Modify /etc/rc.local and Add the following between "fi" and "exit 0"
''
python3 /WHERE-EVER-YOU-PUT-IT/network_display.py &
''

Modify /etc/network/interfaces and add
''
iface eth0 inet static
    address 192.168.169.249
    netmask 255.255.255.0
''


Raspberry Pi running as the Server
Files needed from repository
network_server.py

Modify /etc/rc.local and Add the following between "fi" and "exit 0"
''
iperf3 -s -p 9000 &
python3 /WHERE-EVER-YOU-PUT-IT/network_server.py &
''

Modify /etc/network/interfaces and add
''
iface eth0 inet static
    address 192.168.169.251
    netmask 255.255.255.0
''

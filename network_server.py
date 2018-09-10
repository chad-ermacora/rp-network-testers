'''
    KootNet Network Testers is a programs to test a Network Connection
    Copyright (C) 2018  Chad Ermacora  chad.ermacora@gmail.com  

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import socket, os
from time import sleep

network_wait = 0

while network_wait == 0:
    try:
        # Create a TCP/IP socket and Bind the socket to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.169.251', 10062)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        network_wait = 1
    except:
        sleep(5)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('\nwaiting for a connection ... \n')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        os.system("sudo shutdown -h now")
    except:
        print("\nConnection Failed?\n")
    finally:
        # Clean up the connection
        connection.close()
# Close again, in case it didn't before... Should never reach this. 
connection.close()
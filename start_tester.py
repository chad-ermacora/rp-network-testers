"""
    'KootNet Ethernet Testers' is a collection of scripts and programs
    to test Ethernet cables and or network routes.
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
"""
from time import sleep
from os import system
from threading import Thread
from operations_modules import threads_access, config_pi, http_server
from operations_modules.display_pi import start_display_server


def start_iperf_server():
    system("/usr/bin/iperf3 -s -p 9000")


threads_access.http_server = Thread(target=http_server.CreateSensorHTTP)
threads_access.http_server.daemon = True
threads_access.http_server.start()

if config_pi.is_iperf_server:
    threads_access.iperf3_server = Thread(target=start_iperf_server)
    threads_access.iperf3_server.daemon = True
    threads_access.iperf3_server.start()
else:
    if config_pi.running_on_rpi:
        threads_access.display_server = Thread(target=start_display_server)
        threads_access.display_server.daemon = True
        threads_access.display_server.start()

while True:
    sleep(600)

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
from operations_modules.app_generic_functions import CreateMonitoredThread
from operations_modules import threads_access, config_pi, http_server
from operations_modules.display_pi import CreateDisplayServer


def start_iperf_server():
    system("/usr/bin/iperf3 -s -p 9000")


threads_access.http_server = CreateMonitoredThread(http_server.CreateSensorHTTP, thread_name="HTTPS Server")
if config_pi.current_config.is_iperf_server:
    threads_access.iperf3_server = CreateMonitoredThread(start_iperf_server, thread_name="iPerf3 Server")
else:
    if config_pi.current_config.running_on_rpi:
        threads_access.display_server = CreateMonitoredThread(CreateDisplayServer, thread_name="Display Server")

while True:
    sleep(600)

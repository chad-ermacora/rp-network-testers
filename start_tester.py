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
import os
from time import sleep
from operations_modules import file_locations
from operations_modules.config_primary import current_config
from operations_modules.app_generic_functions import CreateMonitoredThread
from operations_modules import config_primary, http_server, app_variables
from operations_modules.interaction_server import CreateInteractiveServer
from operations_modules.hardware_access import hardware_access


def enable_fake_hw_clock():
    os.system("bash " + file_locations.enable_fake_hw_clock_script)


def start_iperf_server():
    os.system("/usr/bin/iperf3 -s -p " + current_config.iperf_port)


if current_config.running_on_rpi:
    enable_fake_hw_clock()

if not os.path.isdir(file_locations.script_folder_path + "/test_results"):
    os.mkdir(file_locations.script_folder_path + "/test_results")

print(" -- HTTP Server Started on port " + str(http_server.flask_http_port))
app_variables.http_server = CreateMonitoredThread(http_server.CreateHTTPServer, thread_name="HTTP Server")
if config_primary.current_config.is_iperf_server:
    print(" -- iPerf 3 Server started on port " + current_config.iperf_port)
    app_variables.iperf3_server = CreateMonitoredThread(start_iperf_server, thread_name="iPerf3 Server")
if config_primary.current_config.running_on_rpi:
    print(" -- Interactive Hardware Server started")
    app_variables.interactive_hw_server = CreateMonitoredThread(CreateInteractiveServer, thread_name="Interactive Server")
    hardware_access.display_message(hardware_access.get_start_message())
else:
    part_1_msg = "\nInteractive Hardware only supported on Raspberry Pis - "
    print(part_1_msg + "Interactive Hardware Server Disabled")
while True:
    sleep(600)

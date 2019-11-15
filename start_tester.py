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
from operations_modules import threads_access, config_primary, http_server
from operations_modules.interaction_server import CreateInteractiveServer
from operations_modules.hardware_access import hardware_access


def start_iperf_server():
    os.system("/usr/bin/iperf3 -s -p " + current_config.iperf_port)


if not os.path.isdir(file_locations.script_folder_path + "/test_results"):
    os.mkdir(file_locations.script_folder_path + "/test_results")

threads_access.http_server = CreateMonitoredThread(http_server.CreateSensorHTTP, thread_name="HTTPS Server")
if config_primary.current_config.is_iperf_server:
    threads_access.iperf3_server = CreateMonitoredThread(start_iperf_server, thread_name="iPerf3 Server")
if config_primary.current_config.running_on_rpi:
    threads_access.interactive_hardware_server = CreateMonitoredThread(CreateInteractiveServer, thread_name="Display Server")
    hardware_access.display_message(hardware_access.get_start_message())
else:
    part_1_msg = "Interactive Hardware not supported on anything besides a Raspberry Pi. "
    print(part_1_msg + "Interactive Hardware Server Disabled.\n")
while True:
    sleep(600)

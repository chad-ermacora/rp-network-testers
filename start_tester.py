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
from operations_modules.logger import primary_logger
from operations_modules import file_locations
from operations_modules import app_variables
from operations_modules import http_server
from operations_modules import schedule_server
from operations_modules.config_primary import current_config
from operations_modules.app_generic_functions import CreateMonitoredThread
from operations_modules.interaction_server import CreateInteractiveServer
from operations_modules.hardware_access import hardware_access


def enable_fake_hw_clock():
    os.system("bash " + file_locations.enable_fake_hw_clock_script)


def start_iperf_server():
    os.system("/usr/bin/iperf3 -s -p " + current_config.iperf_port)


primary_logger.info(" -- Starting HTTP Server on port " + str(app_variables.flask_http_port))
app_variables.http_server = CreateMonitoredThread(http_server.CreateHTTPServer, thread_name="HTTP Server")

if current_config.schedule_run_every_minutes and current_config.schedule_run_every_minutes_enabled:
    primary_logger.info(" -- Starting Scheduled Tests Server ")
    schedule_function = schedule_server.start_run_every_minutes
    app_variables.scheduled_test_run_server = CreateMonitoredThread(schedule_function, thread_name="Scheduled Server")

if current_config.is_iperf_server:
    primary_logger.info(" -- Starting iPerf 3 Server on port " + current_config.iperf_port)
    app_variables.iperf3_server = CreateMonitoredThread(start_iperf_server, thread_name="iPerf3 Server")

if current_config.running_on_rpi:
    enable_fake_hw_clock()
    primary_logger.info(" -- Starting Interactive Hardware Server")
    app_variables.interactive_hw_server = CreateMonitoredThread(CreateInteractiveServer, thread_name="HW Server")
    hardware_access.display_message(hardware_access.get_button_functions_message())

while True:
    sleep(600)

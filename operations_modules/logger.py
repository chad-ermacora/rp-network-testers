"""
    KootNet Sensors is a collection of programs and scripts to deploy,
    interact with, and collect readings from various Sensors.
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

--------------------------------------------------------------------------
Logger used throughout the program. Configuration options listed below.

DEBUG - Detailed information, typically of interest only when diagnosing problems. test
INFO - Confirmation that things are working as expected.
WARNING - An indication that something unexpected happened, or indicative of some problem in the near future
ERROR - Due to a more serious problem, the software has not been able to perform some function.
CRITICAL - A serious error, indicating that the program itself may be unable to continue running.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from operations_modules import file_locations

if not os.path.exists(os.path.dirname(file_locations.log_directory)):
    os.makedirs(os.path.dirname(file_locations.log_directory))

max_log_lines_return = 250
logging_level = logging.DEBUG


def initialize_logger():
    formatter = logging.Formatter("%(asctime)s - %(levelname)s:  %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler_main = RotatingFileHandler(file_locations.primary_log, maxBytes=256000, backupCount=5)
    file_handler_main.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    primary_logger.addHandler(file_handler_main)
    primary_logger.addHandler(stream_handler)
    primary_logger.setLevel(logging_level)


def get_number_of_log_entries(log_file):
    """ Opens provided log file location and returns the amount of log entries in it. """
    with open(log_file, "r") as log_content:
        log_lines = log_content.readlines()
        return len(log_lines)


def get_sensor_log(log_file):
    """ Opens provided log file location and returns its content. """
    with open(log_file, "r") as log_content:
        log_lines = log_content.readlines()
        if max_log_lines_return:
            log_lines = log_lines[-max_log_lines_return:]
        log_lines.reverse()

        return_log = ""
        for log in log_lines:
            return_log += log
        return return_log


def clear_primary_log():
    """ Clears all Primary Sensor Log. """
    with open(file_locations.primary_log, "w") as log_content:
        log_content.write("")


primary_logger = logging.getLogger("PrimaryLog")
initialize_logger()

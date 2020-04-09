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
from operations_modules.logger import primary_logger
from operations_modules.config_primary import current_config
from operations_modules import run_commands


def _start_run_at_date(run_on_date_time):
    if current_config.schedule_run_on_boot:
        pass


def start_run_every_minutes():
    if current_config.schedule_run_on_boot:
        run_commands.start_mtr()
        run_commands.start_iperf()

    if current_config.schedule_run_every_minutes < 5:
        primary_logger.warning("Scheduled times cannot be less then 5 minutes")
        current_config.schedule_run_every_minutes = 5

    while True:
        try:
            if current_config.schedule_run_every_minutes_enabled:
                sleep(current_config.schedule_run_every_minutes * 60)
                run_commands.start_mtr()
                run_commands.start_iperf()
            else:
                sleep(300)
        except Exception as error:
            primary_logger.error("Error Running Scheduled Test: " + str(error))

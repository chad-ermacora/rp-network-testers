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
from threading import Thread
from operations_modules.config_primary import current_config
from operations_modules import run_commands


def start_scheduled_runs():
    if current_config.schedule_run_every_minutes:
        minutes = current_config.schedule_run_every_minutes
        run_every_minutes_thread = Thread(target=_start_run_every_minutes, args=minutes)
        run_every_minutes_thread.daemon = True
        run_every_minutes_thread.start()

    if current_config.schedule_run_1_enabled:
        pass
    if current_config.schedule_run_2_enabled:
        pass
    if current_config.schedule_run_3_enabled:
        pass
    if current_config.schedule_run_4_enabled:
        pass


def _start_run_at_date(run_on_date_time):
    if current_config.schedule_run_on_boot:
        pass


def _start_run_every_minutes(minutes):
    if current_config.schedule_run_on_boot:
        run_commands.start_mtr()
        run_commands.start_iperf()

    sleep_time_seconds = minutes * 60
    if minutes < 5:
        print("Scheduled times cannot be less then 5 minutes")
        sleep_time_seconds = 300
    while True:
        try:
            sleep(sleep_time_seconds)
            run_commands.start_mtr()
            run_commands.start_iperf()
        except Exception as error:
            print("Problem Running Scheduled Test: " + str(error))

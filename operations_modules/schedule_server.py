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
from datetime import datetime
from operations_modules.logger import primary_logger
from operations_modules import app_variables
from operations_modules.config_primary import current_config
from operations_modules import run_commands


def start_run_at_date():
    app_variables.restart_run_once_test_server = 0
    while not app_variables.restart_run_once_test_server:
        while not current_config.schedule_run_once_enabled:
            sleep(30)

        try:
            utc_now = datetime.utcnow()
            scheduled_runtime = datetime.strptime(current_config.schedule_run_once_at_time, "%Y-%m-%dT%H:%M")
            sleep_time = (scheduled_runtime - utc_now).total_seconds()

            if sleep_time > 0:
                total_sleep_time = 0
                skip_test_runs = 0
                primary_logger.info("Single Run Tests set to run in: " + str(sleep_time) + " Seconds")
                while total_sleep_time < sleep_time:
                    sleep(5)
                    total_sleep_time += 5
                    if app_variables.restart_run_once_test_server:
                        skip_test_runs = 1
                        sleep_time = total_sleep_time
                if not skip_test_runs:
                    run_commands.start_mtr()
                    run_commands.start_iperf()
            else:
                primary_logger.warning("Single Run Tests Date & Time has already passed, disabling Run Once Schedule")
                current_config.schedule_run_once_enabled = 0
                current_config.write_config_to_file()
        except Exception as error:
            primary_logger.error("Single scheduled test run: " + str(error))
            current_config.schedule_run_once_enabled = 0


def start_run_every_minutes():
    if current_config.schedule_run_on_boot:
        run_commands.start_mtr()
        run_commands.start_iperf()

    if current_config.schedule_run_every_minutes < 5:
        primary_logger.warning("Scheduled times cannot be less then 5 minutes")
        current_config.schedule_run_every_minutes = 5

    if current_config.schedule_run_every_minutes_enabled:
        log_msg = "Tests scheduled to run every " + str(current_config.schedule_run_every_minutes) + " minutes"
        primary_logger.info(log_msg)

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

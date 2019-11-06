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
import time
import requests
from threading import Thread


class CreateMonitoredThread:
    def __init__(self, function, args=None, thread_name="Generic Thread", max_restart_tries=5):
        self.is_running = True
        self.function = function
        self.args = args
        self.thread_name = thread_name

        self.current_restart_count = 0
        self.max_restart_count = max_restart_tries

        self._thread_and_monitor()

    def _thread_and_monitor(self):
        try:
            monitored_thread = Thread(target=self._worker_thread_and_monitor)
            monitored_thread.daemon = True
            monitored_thread.start()
        except Exception as error:
            print(str(error))

    def _worker_thread_and_monitor(self):
        if self.args is not None:
            monitored_thread = Thread(target=self.function, args=self.args)
        else:
            monitored_thread = Thread(target=self.function)
        monitored_thread.daemon = True
        monitored_thread.start()

        while True:
            time.sleep(30)
            if not monitored_thread.is_alive():
                self.is_running = False
                self.current_restart_count += 1
                if self.current_restart_count < self.max_restart_count:
                    if self.args is not None:
                        monitored_thread = Thread(target=self.function, args=self.args)
                    else:
                        monitored_thread = Thread(target=self.function)
                    monitored_thread.daemon = True
                    monitored_thread.start()
                    self.is_running = True
                else:
                    log_msg = self.thread_name + " has attempted to restart " + str(self.current_restart_count)
                    print(log_msg + " Times.  No further restart attempts will be made.")
                    while True:
                        time.sleep(600)


def get_file_content(load_file, open_type="r"):
    """ Loads provided file and returns it's content. """
    if os.path.isfile(load_file):
        try:
            loaded_file = open(load_file, open_type)
            file_content = loaded_file.read()
            loaded_file.close()
        except Exception as error:
            print(str(error))
            file_content = ""
        return file_content


def write_file_to_disk(file_location, file_content, open_type="w"):
    """ Writes provided file and content to local disk. """
    try:
        write_file = open(file_location, open_type)
        write_file.write(file_content)
        write_file.close()
    except Exception as error:
        print("Write to Disk Error: " + str(error))


def send_command(url):
    """ Sends command URL using requests. """
    try:
        requests.get(url=url, timeout=5, headers={'Connection': 'close'}, verify=False)
        print("Command '" + url + "' OK")
        return True
    except Exception as error:
        print(str(error))
        return False

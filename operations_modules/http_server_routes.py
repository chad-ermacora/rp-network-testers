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
from flask import Blueprint, render_template, send_file
from operations_modules import file_locations
from operations_modules import app_generic_functions
from operations_modules import app_variables
from operations_modules import run_commands
from operations_modules.config_primary import current_config

http_routes = Blueprint("http_routes", __name__)


@http_routes.route("/")
@http_routes.route("/index.html")
def html_root():
    tests_running_msg = ""
    button_disabled = ""
    if current_config.tests_running:
        tests_running_msg = "Running Tests Please Wait ..."
        button_disabled = "disabled"
    return render_template("index.html",
                           TestsRunning=tests_running_msg,
                           DisabledButton=button_disabled,
                           OSVersion=app_generic_functions.get_os_name_version(),
                           KootnetVersion=current_config.app_version,
                           Results_MTR=str(app_variables.raw_previous_mtr),
                           Results_iPerf=str(app_variables.raw_previous_iperf),
                           InteractiveIP=current_config.display_ip,
                           ServerIP=current_config.remote_tester_ip,
                           iPerfPort=current_config.iperf_port,
                           MTRCount=current_config.mtr_run_count)


@http_routes.route("/mui.min.css")
def mui_min_css():
    return send_file(file_locations.mui_min_css)


@http_routes.route("/mui.min.js")
def mui_min_js():
    return send_file(file_locations.mui_min_js)


@http_routes.route("/mui-colors.min.css")
def mui_colors_min_css():
    return send_file(file_locations.mui_colors_min_css)


@http_routes.route("/StartTests", methods=["POST"])
def start_tests():
    if current_config.is_iperf_server:
        app_generic_functions.send_command("https://" + current_config.display_ip + "/StartTests")
        return render_template("message_return.html",
                               URL="https://" + current_config.display_ip,
                               TextMessage="Re-Directing to Display Server")
    else:
        app_generic_functions.thread_function(run_commands.start_all_tests)
    return html_root()

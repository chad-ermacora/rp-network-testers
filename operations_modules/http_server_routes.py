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
from socket import gethostname
from flask import request, Blueprint, render_template, send_file
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

    mtr_text = "Last Run\n" + str(app_variables.last_run_mtr) + "\n(DD/MM/YY - HH:MM)\n\n" + \
               str(app_variables.raw_previous_mtr)
    iperf_text = "Last Run\n" + str(app_variables.last_run_iperf) + "\n(DD/MM/YY - HH:MM)\n\n" + \
                 str(app_variables.raw_previous_iperf)
    return render_template("index.html",
                           TestsRunning=tests_running_msg,
                           IPHostname=str(gethostname()),
                           DisabledButton=button_disabled,
                           OSVersion=app_generic_functions.get_os_name_version(),
                           KootnetVersion=current_config.app_version,
                           Results_MTR=mtr_text,
                           Results_iPerf=iperf_text,
                           InteractiveIP=current_config.interactive_unit_ip,
                           ServerIP=current_config.remote_tester_ip,
                           iPerfPort=current_config.iperf_port,
                           MTRCount=current_config.mtr_run_count)


@http_routes.route("/UpdateProgram")
def update_program():
    app_generic_functions.thread_function(os.system, args="bash " + file_locations.http_upgrade_script)
    return render_template("message_return.html", URL="/",
                           TextMessage="Standard Upgrade in Progress",
                           TextMessage2="Please wait ...")


@http_routes.route("/UpdateProgramDev")
def update_program_development():
    app_generic_functions.thread_function(os.system, args="bash " + file_locations.http_upgrade_script + " dev")
    return render_template("message_return.html", URL="/",
                           TextMessage="Development Upgrade in Progress",
                           TextMessage2="Please wait ...")


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
    if request.form.get("run_mtr") is not None and request.form.get("run_iperf") is not None:
        app_generic_functions.thread_function(run_commands.start_all_tests)
    elif request.form.get("run_mtr") is not None:
        app_generic_functions.thread_function(run_commands.start_mtr)
    elif request.form.get("run_iperf") is not None:
        app_generic_functions.thread_function(run_commands.start_iperf)
    else:
        return render_template("message_return.html", URL="/", TextMessage="Error Starting Tests: Bad POST Data")
    return html_root()


@http_routes.route("/EditConfiguration", methods=["POST", "GET"])
def edit_configuration():
    if request.form.get("ip_hostname") is not None:
        new_hostname = str(request.form.get("ip_hostname"))
        if app_generic_functions.hostname_is_valid(new_hostname):
            os.system("hostname " + new_hostname)

    if request.form.get("iperf_server_ip") is not None:
        current_config.remote_tester_ip = str(request.form.get("iperf_server_ip"))
    else:
        current_config.remote_tester_ip = "192.168.169.251"

    if request.form.get("iperf_port") is not None:
        current_config.iperf_port = str(request.form.get("iperf_port"))
    else:
        current_config.iperf_port = "9000"

    if request.form.get("mtr_run_count") is not None:
        current_config.mtr_run_count = str(request.form.get("mtr_run_count"))
    else:
        current_config.mtr_run_count = "10"
    current_config.write_config_to_file()
    return html_root()


@http_routes.route("/EditEthernetIPv4", methods=["POST"])
def edit_eth_ipv4_network():
    if request.form.get("ip_hostname") is not None:
        current_config.interactive_unit_ip = str(request.form.get("interactive_unit_ip"))
    else:
        current_config.interactive_unit_ip = "192.168.169.249"

    return html_root()


@http_routes.route("/EditWifiIPv4", methods=["POST"])
def edit_wifi_ipv4_network():
    if request.form.get("ip_hostname") is not None:
        current_config.interactive_unit_ip = str(request.form.get("interactive_unit_ip"))
    else:
        current_config.interactive_unit_ip = "192.168.169.249"

    return html_root()

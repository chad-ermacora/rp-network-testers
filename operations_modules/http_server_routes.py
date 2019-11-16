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
import shutil
from socket import gethostname
from flask import request, Blueprint, render_template, send_file
from operations_modules import file_locations
from operations_modules import app_generic_functions
from operations_modules import app_variables
from operations_modules import run_commands
from operations_modules import network_ip
from operations_modules import network_wifi
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

    iperf_server_enabled = ""
    if current_config.is_iperf_server:
        iperf_server_enabled = "checked"
    wave_share_27_enabled = ""
    if current_config.installed_interactive_hw["WaveShare27"]:
        wave_share_27_enabled = "checked"

    ethernet_dhcp = ""
    if current_config.local_ethernet_dhcp:
        ethernet_dhcp = "checked"
    wireless_dhcp = ""
    if current_config.local_wireless_dhcp:
        wireless_dhcp = "checked"

    mtr_results = ""
    if app_variables.previous_mtr_results:
        mtr_results = app_variables.previous_mtr_start_text + str(app_variables.previous_mtr_results)
    iperf_results = ""
    if app_variables.previous_iperf_results:
        iperf_results = app_variables.previous_iperf_start_text + str(app_variables.previous_iperf_results)

    return render_template("index.html",
                           TestsRunning=tests_running_msg,
                           IPHostname=str(gethostname()),
                           DisabledButton=button_disabled,
                           OSVersion=app_generic_functions.get_os_name_version(),
                           KootnetVersion=current_config.app_version,
                           Results_MTR=mtr_results,
                           Results_iPerf=iperf_results,
                           CheckediPerfServer=iperf_server_enabled,
                           InteractiveIP=current_config.local_ethernet_ip,
                           ServerIP=current_config.remote_tester_ip,
                           iPerfPort=current_config.iperf_port,
                           MTRCount=current_config.mtr_run_count,
                           CheckedWaveShare27EInk=wave_share_27_enabled,
                           EthernetCheckedDHCP=ethernet_dhcp,
                           EthernetIPv4Address=current_config.local_ethernet_ip,
                           EthernetIPv4Subnet=current_config.local_ethernet_subnet,
                           EthernetIPGateway=current_config.local_ethernet_gateway,
                           EthernetIPDNS1=current_config.local_ethernet_dns1,
                           EthernetIPDNS2=current_config.local_ethernet_dns2,
                           WirelessCheckedDHCP=wireless_dhcp,
                           WirelessIPv4Address=current_config.local_wireless_ip,
                           WirelessIPv4Subnet=current_config.local_wireless_subnet,
                           WirelessIPGateway=current_config.local_wireless_gateway,
                           WirelessIPDNS1=current_config.local_wireless_dns1,
                           WirelessIPDNS2=current_config.local_wireless_dns2)


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


@http_routes.route("/ReStart")
def restart_program():
    app_generic_functions.thread_function(os.system, args="systemctl restart KootnetEthServer")
    return render_template("message_return.html", URL="/", TextMessage="Re-Starting Program",
                           TextMessage2="You will automatically be redirected to home in 10 seconds")


@http_routes.route("/Shutdown")
def shutdown_system():
    app_generic_functions.thread_function(os.system, args="shutdown now")
    return render_template("message_return.html", URL="/", TextMessage="Shutting Down Unit",
                           TextMessage2="Please wait 15 seconds before removing power")


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


@http_routes.route("/EditConfiguration", methods=["POST"])
def edit_configuration():
    if request.form.get("ip_hostname") is not None:
        new_hostname = str(request.form.get("ip_hostname"))
        if app_generic_functions.hostname_is_valid(new_hostname):
            os.system("hostname " + new_hostname)

    if request.form.get("checkbox_iperf_server") is not None:
        current_config.is_iperf_server = 1
    else:
        current_config.is_iperf_server = 0

    if request.form.get("remote_test_server_ip") is not None:
        current_config.remote_tester_ip = str(request.form.get("remote_test_server_ip"))
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


@http_routes.route("/EditInstalledHardware", methods=["POST"])
def edit_installed_hardware():
    if request.form.get("checkbox_waveshare_2_7_e_ink") is not None:
        current_config.installed_interactive_hw["WaveShare27"] = 1
    else:
        current_config.installed_interactive_hw["WaveShare27"] = 0
    current_config.write_installed_hardware_to_file()
    return render_template("message_return.html", URL="/", TextMessage="Installed Hardware Saved",
                           TextMessage2="Please reboot the device for settings to take effect")


@http_routes.route("/EditEthernetIPv4", methods=["POST"])
def edit_eth_ipv4_network():
    if current_config.running_on_rpi:
        if request.form.get("ethernet_ip_dhcp") is not None:
            message = "You must reboot for all settings to take effect."
            dhcpcd_template = app_generic_functions.get_file_content(file_locations.dhcpcd_config_file_template)
            dhcpcd_template = dhcpcd_template.replace("{{ StaticIPSettings }}", "")
            app_generic_functions.write_file_to_disk(file_locations.dhcpcd_config_file, dhcpcd_template)
            return render_template("message_return.html", URL="/", TextMessage="Ethernet Settings Applied",
                                   TextMessage2=message)
        config_ok = set_html_config_ipv4(request)
        if config_ok:
            return render_template("message_return.html", URL="/", TextMessage="Ethernet Configuration OK",
                                   TextMessage2="You must reboot the device for settings to take effect")
        return render_template("message_return.html", URL="/", TextMessage="Bad Configuration Options",
                               TextMessage2="Please check your Ethernet configuration carefully and try again")
    return render_template("message_return.html", URL="/", TextMessage="OS Not Supported",
                           TextMessage2="Ethernet Network Configuration not supported on current OS")


@http_routes.route("/EditWifiIPv4", methods=["POST"])
def edit_wifi_ipv4_network():
    if current_config.running_on_rpi:
        # set_html_config_wifi(request)
        set_html_config_ipv4(request)
        return html_root()
    return render_template("message_return.html", URL="/", TextMessage="OS Not Supported",
                           TextMessage2="Wireless Network Configuration not supported on current OS")


def set_html_config_wifi(html_request):
    if current_config.running_on_rpi:
        return html_root()
    return render_template("message_return.html", URL="/", TextMessage="OS Not Supported",
                           TextMessage2="Wireless Network Configuration not supported on current OS")


def set_html_config_ipv4(html_request, wireless_type=False):
    print("Starting HTML IPv4 Configuration Update for Ethernet or Wireless.  Wireless = " + str(wireless_type))
    network_template = app_generic_functions.get_file_content(file_locations.dhcpcd_config_file_template)
    html_request_variable_names = ["ethernet_ip_address", "ethernet_ip_subnet", "ethernet_ip_gateway",
                                   "ethernet_ip_dns1", "ethernet_ip_dns2"]
    if wireless_type:
        network_template = app_generic_functions.get_file_content(file_locations.wifi_config_file_template)
        html_request_variable_names = ["wifi_ip_address", "wifi_ip_subnet", "wifi_ip_gateway",
                                       "wifi_ip_dns1", "wifi_ip_dns2"]

    ip_address = html_request.form.get(html_request_variable_names[0])
    ip_subnet_mask = html_request.form.get(html_request_variable_names[1])
    ip_gateway = html_request.form.get(html_request_variable_names[2])
    ip_dns1 = html_request.form.get(html_request_variable_names[3])
    ip_dns2 = html_request.form.get(html_request_variable_names[4])

    for new_variable in [ip_address, ip_subnet_mask]:
        if app_generic_functions.check_for_none_and_blank(new_variable):
            return False

    if wireless_type:
        if current_config.local_wireless_dhcp:
            dhcp = True
        else:
            dhcp = False

        current_config.local_wireless_ip = ip_address.strip()
        current_config.local_wireless_subnet = ip_subnet_mask.strip()
        current_config.local_wireless_gateway = ip_gateway.strip()
        current_config.local_wireless_dns1 = ip_dns1.strip()
        current_config.local_wireless_dns2 = ip_dns2.strip()
        ip_network_text2 = "interface " + current_config.local_ethernet_adapter_name + "\nstatic ip_address=" + \
                           current_config.local_ethernet_ip + current_config.local_ethernet_subnet + \
                           "\nstatic routers=" + current_config.local_ethernet_gateway + \
                           "\nstatic domain_name_servers=" + current_config.local_ethernet_dns1 + " " + \
                           current_config.local_ethernet_dns2
        for network_setting in [current_config.local_ethernet_adapter_name, current_config.local_ethernet_ip,
                                current_config.local_ethernet_subnet, current_config.local_ethernet_gateway]:
            if app_generic_functions.check_for_none_and_blank(network_setting):
                ip_network_text2 = ""

    else:
        if current_config.local_ethernet_dhcp:
            dhcp = True
        else:
            dhcp = False

        current_config.local_ethernet_ip = ip_address.strip()
        current_config.local_ethernet_subnet = ip_subnet_mask.strip()
        current_config.local_ethernet_gateway = ip_gateway.strip()
        current_config.local_ethernet_dns1 = ip_dns1.strip()
        current_config.local_ethernet_dns2 = ip_dns2.strip()
        ip_network_text2 = "interface " + current_config.local_wireless_adapter_name + "\nstatic ip_address=" + \
                           current_config.local_wireless_ip + current_config.local_wireless_subnet + \
                           "\nstatic routers=" + current_config.local_wireless_gateway + \
                           "\nstatic domain_name_servers=" + current_config.local_wireless_dns1 + " " + \
                           current_config.local_wireless_dns2
        for network_setting in [current_config.local_wireless_adapter_name, current_config.local_wireless_ip,
                                current_config.local_wireless_subnet, current_config.local_wireless_gateway]:
            if app_generic_functions.check_for_none_and_blank(network_setting):
                ip_network_text2 = ""

    if dhcp:
        ip_network_text = ""
    else:
        ip_network_text = "interface eth0\nstatic ip_address=" + ip_address + ip_subnet_mask + \
                          "\nstatic routers=" + ip_gateway + "\nstatic domain_name_servers=" + ip_dns1 + " " + ip_dns2
    network_template = network_template.replace("{{ StaticIPSettings }}", ip_network_text + "\n\n" + ip_network_text2)
    network_ip.write_ipv4_config_to_file(network_template)
    shutil.chown(file_locations.dhcpcd_config_file, "root", "netdev")
    os.chmod(file_locations.dhcpcd_config_file, 0o664)
    return True

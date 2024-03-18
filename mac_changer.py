import subprocess
import optparse
import re


def get_current_mac(interface):
    ifconfig_interface_results = subprocess.check_output(["ifconfig", interface])
    mac_address_search_results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_interface_results))
    if mac_address_search_results:
        return mac_address_search_results.group(0)
    else:
        print("[-] Could not read MAC address")
        exit(0)


def get_mac_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (arguments, options) = parser.parse_args()
    ifconfig_results = subprocess.check_output(["ifconfig"])
    all_interfaces = re.findall(r"[a-z]{3,4}\d", str(ifconfig_results))
    if (not arguments.interface or not bool(re.match(r"^[a-z]{3,4}\d$", arguments.interface)) or
            arguments.interface not in all_interfaces):
        print("[-] Invalid input; Please specify an interface; Use -h or --help for more info")
        exit(0)
    elif not arguments.new_mac or not bool(re.match(r"^\w\w:\w\w:\w\w:\w\w:\w\w:\w\w$", arguments.new_mac)):
        print("[-] Invalid input; Please specify a MAC address; Use -h or --help for more info")
        exit(0)
    else:
        return arguments


def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    current_mac = get_current_mac(arguments.interface)
    if current_mac == new_mac:
        print("[+] MAC address of " + interface + " successfully changed to " + new_mac)
    else:
        print("[-] Could not change MAC address")
        exit(0)


arguments = get_mac_arguments()
current_mac = get_current_mac(arguments.interface)
change_mac(arguments.interface, arguments.new_mac)

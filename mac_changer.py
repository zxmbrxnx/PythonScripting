#!/usr/bin/env python3

import argparse, sys, signal, subprocess, re
from termcolor import colored

def def_handler(sig, frame):
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler) # ctrl + c

def get_arguments():
    parser = argparse.ArgumentParser(description=colored('MAC changer tool by @zxmbrxnx', 'red'))
    parser.add_argument('-i', '--interface', dest='interface', required=True, metavar='', help='Interface to change MAC address')
    parser.add_argument('-m', '--mac', dest='mac', metavar='', help='New MAC address')
    parser.add_argument('-p', '--permanent', dest='permanent', action='store_true', help='Restore MAC address to permanent')
    return parser.parse_args()

def is_valid_args(interface, mac):
    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    is_valid_mac = re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac)
    return not is_valid_interface or not is_valid_mac

def change_mac(interface, mac):
    if is_valid_args(interface, mac):
        print(colored('[!] Invalid arguments', 'red'))
        sys.exit(1)

    print(colored(f'Changing MAC address for {interface} to {mac}', 'green'))
    
    subprocess.run(['ifconfig', interface, 'down'])
    subprocess.run(['ifconfig', interface, 'hw', 'ether', mac])
    subprocess.run(['ifconfig', interface, 'up'])

    print(colored(f'[+] MAC address for {interface} changed to {mac}', 'green'))

def restore_mac(interface):
    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    if not is_valid_interface:
        print(colored('[!] Invalid interface', 'red'))
        sys.exit(1)
    
    print(colored(f'Restoring MAC address for {interface} to permanent', 'green'))
    subprocess.run(['ifconfig', interface, 'down'])
    subprocess.run(['macchanger', '-p', interface])
    subprocess.run(['ifconfig', interface, 'up'])
    print(colored(f'[+] MAC address for {interface} restored to permanent', 'green'))

def main():
    args = get_arguments()
    if args.permanent:
        restore_mac(args.interface)
    else:
        change_mac(args.interface, args.mac)

if __name__ == '__main__':
    main()
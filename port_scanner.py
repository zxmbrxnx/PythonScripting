#!/usr/bin/env python3

import socket, argparse, sys, signal, time
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

open_sockets = []

def def_handler(sig, frame):
    print(colored('\n[!] Closing sockets...', 'red'))
    for socket in open_sockets:
        socket.close()
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler) # ctrl + c

def get_arguments():
    parser = argparse.ArgumentParser(description=colored('Port scanner tool by @zxmbrxnx', 'red'))
    parser.add_argument('-t', '--target', dest='target', required=True, metavar='', help='Target IP')
    parser.add_argument('-p', '--port', dest='port', metavar='', help='Port range to scan (e.g. 1-1024)')
    options = parser.parse_args()

    if not options.port:
        options.port = '1-1024'

    return options.target, options.port

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    open_sockets.append(s)
    return s

def port_scanner(port, host):
    s = create_socket()
    try:
        s.connect((host, port))
        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        response = s.recv(1024).decode(errors='ignore').split('\r\n')[0]
        print(f'{port} \topen\t{response}')
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        s.close()

def parse_ports(ports_str):
    if '-' in ports_str:
        start, end = map(int, ports_str.split('-'))
        if start > end:
            print(colored('[!] Invalid port range', 'red'))
            sys.exit(1)
        return range(start, end + 1)
    elif ',' in ports_str:
        return map(int, ports_str.split(','))

    elif not ports_str.isdigit():
        print(colored('[!] Invalid port', 'red'))
        sys.exit(1)

    return [int(ports_str)]

def scan_ports(target, ports):
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in ports:
            executor.submit(port_scanner, port, target)

def main():
    target, ports_str = get_arguments()
    ports = parse_ports(ports_str)
    print(colored(f'Scan report for {target}', 'green'))
    print(colored('PORT\tSTATE\tRESPONSE', 'green'))
    start_time = time.time()
    scan_ports(target, ports)
    end_time = time.time()
    print(colored(f'\nScan completed in {end_time - start_time:.2f}s', 'green'))

if __name__ == '__main__':
    main()
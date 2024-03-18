import socket
import argparse

def scan_port(host, port, protocol):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 't' else socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        sock.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        sock.close()

def parse_args():
    parser = argparse.ArgumentParser(description='Tiny port scanner')
    parser.add_argument('host', help='Host to scan')
    parser.add_argument('-p', '--ports', help='Range of ports to scan')
    parser.add_argument('-u', '--udp', action='store_true', help='UDP scan')
    parser.add_argument('-t', '--tcp', action='store_true', help='TCP scan')
    return parser.parse_args()

def main():
    args = parse_args()
    protocol = 'u' if args.udp else 't'
    ports = args.ports.split('-') if '-' in args.ports else [args.ports, args.ports]
    for port in range(int(ports[0]), int(ports[1]) + 1):
        if scan_port(args.host, port, protocol):
            print(f'Port {port} is open')
        else:
            print(f'Port {port} is closed')

if __name__ == '__main__':
    main()
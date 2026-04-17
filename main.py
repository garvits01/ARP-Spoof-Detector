import argparse
from scapy.all import get_if_list
from detector import ARPSpoofDetector

def main():
    parser = argparse.ArgumentParser(description="ARP Spoof Detector")
    parser.add_argument(
        "-i", "--interface",
        required=False,  # Changed from True to False
        help="Network interface to monitor (e.g. eth0, wlan0, en0)"
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="Print available interfaces and exit"
    )
    args = parser.parse_args()

    # 1. Check if the user just wants to list interfaces
    if args.list_interfaces:
        print("Available interfaces:")
        interfaces = get_if_list()
        for iface in interfaces:
            print(f"  - {iface}")
        return

    # 2. If not listing, enforce that the interface argument is provided
    if not args.interface:
        parser.error("the following arguments are required: -i/--interface (unless using --list-interfaces)")

    # 3. Proceed with the detector
    detector = ARPSpoofDetector(interface=args.interface)
    detector.start()

if __name__ == "__main__":
    main()
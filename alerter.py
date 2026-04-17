import logging
import datetime
from colorama import Fore, Style, init

init(autoreset=True)

logging.basicConfig(
    filename="arp_alerts.log",
    level=logging.WARNING,
    format="%(asctime)s  %(levelname)s  %(message)s"
)

def alert(ip: str, old_mac: str, new_mac: str, packet_summary: str) -> None:
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # Terminal — red, hard to miss
    print(
        f"\n{Fore.RED}[!] ARP SPOOF DETECTED  {timestamp}{Style.RESET_ALL}\n"
        f"    IP      : {ip}\n"
        f"    Known   : {old_mac}\n"
        f"    Claimed : {new_mac}\n"
        f"    Packet  : {packet_summary}"
    )

    # Persistent log file
    logging.warning(
        f"SPOOF ip={ip} known_mac={old_mac} claimed_mac={new_mac}"
    )

def info(msg: str) -> None:
    print(f"{Fore.CYAN}[*] {msg}{Style.RESET_ALL}")

def warn(msg: str) -> None:
    print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")
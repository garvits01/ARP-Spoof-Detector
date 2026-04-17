import threading
from scapy.all import sniff, ARP, Ether, get_if_hwaddr
from alerter import alert, info, warn
from whitelist import STATIC_WHITELIST


class ARPSpoofDetector:
    def __init__(self, interface: str, iface_whitelist: bool = True):
        self.interface = interface
        self.lock = threading.Lock()

        # Seed table with static whitelist entries
        self.arp_table: dict[str, str] = dict(STATIC_WHITELIST)

        # Optionally trust the detector machine's own interface MAC
        if iface_whitelist:
            try:
                own_mac = get_if_hwaddr(interface)
                info(f"Own interface MAC: {own_mac} (trusted)")
            except Exception:
                pass  # non-fatal

        self.alert_count = 0
        self.packet_count = 0

    # ------------------------------------------------------------------ #
    # Core callback — called by Scapy for every matching packet           #
    # ------------------------------------------------------------------ #
    def _process_packet(self, pkt) -> None:
        # We only care about ARP replies (op=2 = "is-at")
        # Requests (op=1 = "who-has") cannot poison the cache
        if not pkt.haslayer(ARP) or pkt[ARP].op != 2:
            return

        self.packet_count += 1

        sender_ip  = pkt[ARP].psrc   # claimed IP
        sender_mac = pkt[ARP].hwsrc  # claimed MAC (lowercase)

        # Ignore broadcast and zero MACs — these are always noise
        if sender_mac in ("ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00"):
            return

        # Ignore packets from our own interface (prevents self-alerts)
        # Scapy's Ether layer gives us the real frame-level source MAC
        if pkt.haslayer(Ether) and pkt[Ether].src == sender_mac:
            try:
                own_mac = get_if_hwaddr(self.interface)
                if sender_mac == own_mac:
                    return
            except Exception:
                pass

        with self.lock:
            if sender_ip not in self.arp_table:
                # First time seeing this IP — learn it
                self.arp_table[sender_ip] = sender_mac
                return

            known_mac = self.arp_table[sender_ip]

            if known_mac != sender_mac:
                # MAC changed — potential spoof
                self.alert_count += 1
                alert(
                    ip=sender_ip,
                    old_mac=known_mac,
                    new_mac=sender_mac,
                    packet_summary=pkt.summary()
                )

                # POLICY CHOICE: update table after alert so repeated
                # attacks on the same IP keep triggering alerts.
                # Comment this out if you want to only alert once per IP.
                # self.arp_table[sender_ip] = sender_mac

    # ------------------------------------------------------------------ #
    # Public interface                                                     #
    # ------------------------------------------------------------------ #
    def start(self) -> None:
        info(f"Sniffing ARP on interface: {self.interface}")
        info(f"Trusted entries loaded: {len(self.arp_table)}")
        info("Press Ctrl+C to stop.\n")

        try:
            sniff(
                iface=self.interface,
                filter="arp",          # BPF filter — kernel drops non-ARP early
                prn=self._process_packet,
                store=False,           # don't buffer packets in RAM
            )
        except PermissionError:
            warn("Root/admin privileges required. Run with sudo.")
        except KeyboardInterrupt:
            self._print_summary()

    def _print_summary(self) -> None:
        print(
            f"\n\nSession summary:\n"
            f"  ARP packets seen : {self.packet_count}\n"
            f"  Alerts fired     : {self.alert_count}\n"
            f"  IPs tracked      : {len(self.arp_table)}"
        )
        print("\nFinal ARP table snapshot:")
        for ip, mac in sorted(self.arp_table.items()):
            print(f"  {ip:<18} {mac}")
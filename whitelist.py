# Hardcode known-good MAC addresses for critical devices.
# This eliminates false positives for your router, NAS, etc.
# Format: { "IP": "MAC (lowercase, colon-separated)" }

STATIC_WHITELIST = {
    "192.168.1.1":   "aa:bb:cc:dd:ee:ff",  # router/gateway
    "192.168.1.100": "11:22:33:44:55:66",  # NAS
}
from scapy.all import sniff, IP, TCP, UDP
import requests
import time

print("🛡️ NIDS Started - Monitoring Network Traffic...")
print("Press Ctrl+C to stop\n")

# Suspicious ports to watch
SUSPICIOUS_PORTS = {
    22: "SSH Brute Force",
    23: "Telnet Access",
    3389: "RDP Access",
    4444: "Metasploit",
    8080: "HTTP Proxy",
    1337: "Hacker Port",
}

# Track port scan attempts
port_scan_tracker = {}
brute_force_tracker = {}

def send_alert(alert):
    print(f"\n🚨 ALERT DETECTED!")
    print(f"   IP: {alert['sourceIp']}")
    print(f"   Threat: {alert['threatType']}")
    print(f"   Port: {alert['port']}")
    print(f"   Severity: {alert['severity']}")
    print(f"   Time: {alert['timestamp']}\n")

def analyze_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        if TCP in packet:
            port = packet[TCP].dport
            protocol = "TCP"
        elif UDP in packet:
            port = packet[UDP].dport
            protocol = "UDP"
        else:
            return

        print(f"From: {src_ip} → To: {dst_ip} | Protocol: {protocol} | Port: {port}")

        # Check 1 - Suspicious Port Detection
        if port in SUSPICIOUS_PORTS:
            alert = {
                "sourceIp": src_ip,
                "threatType": SUSPICIOUS_PORTS[port],
                "port": port,
                "severity": "HIGH",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            send_alert(alert)

        # Check 2 - Port Scan Detection
        # If same IP hits more than 5 different ports = port scanning!
        if src_ip not in port_scan_tracker:
            port_scan_tracker[src_ip] = set()
        port_scan_tracker[src_ip].add(port)

        if len(port_scan_tracker[src_ip]) > 5:
            alert = {
                "sourceIp": src_ip,
                "threatType": "Port Scanning Detected",
                "port": port,
                "severity": "HIGH",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            send_alert(alert)
            port_scan_tracker[src_ip] = set()  # Reset tracker

        # Check 3 - Brute Force Detection
        # If same IP hits same port more than 3 times = brute force!
        key = f"{src_ip}:{port}"
        if key not in brute_force_tracker:
            brute_force_tracker[key] = 0
        brute_force_tracker[key] += 1

        if brute_force_tracker[key] > 3:
            alert = {
                "sourceIp": src_ip,
                "threatType": "Brute Force Attempt",
                "port": port,
                "severity": "CRITICAL",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            send_alert(alert)
            brute_force_tracker[key] = 0  # Reset tracker

# Capture 50 packets
sniff(prn=analyze_packet, count=50)

print("\n✅ Capture Complete!")
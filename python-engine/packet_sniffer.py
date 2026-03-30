from scapy.all import sniff, IP, TCP, UDP
import requests
import time

print("🛡️ NIDS Started - Monitoring Network Traffic...")
print("Press Ctrl+C to stop\n")

SPRING_BOOT_URL = "http://localhost:8080/api/alerts/add"

SUSPICIOUS_PORTS = {
    22: "SSH Brute Force",
    23: "Telnet Access",
    3389: "RDP Access",
    4444: "Metasploit",
    8080: "HTTP Proxy",
    1337: "Hacker Port",
}

port_scan_tracker = {}
brute_force_tracker = {}

def send_alert(alert):
    try:
        response = requests.post(SPRING_BOOT_URL, json=alert)
        print(f"🚨 ALERT SENT TO SPRING BOOT!")
        print(f"   IP: {alert['sourceIp']}")
        print(f"   Threat: {alert['threatType']}")
        print(f"   Severity: {alert['severity']}")
        print(f"   Status: {response.status_code}\n")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

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

        # Check 1 - Suspicious Port
        if port in SUSPICIOUS_PORTS:
            send_alert({
                "sourceIp": src_ip,
                "threatType": SUSPICIOUS_PORTS[port],
                "port": str(port),
                "severity": "HIGH"
            })

        # Check 2 - Port Scan Detection
        if src_ip not in port_scan_tracker:
            port_scan_tracker[src_ip] = set()
        port_scan_tracker[src_ip].add(port)

        if len(port_scan_tracker[src_ip]) > 5:
            send_alert({
                "sourceIp": src_ip,
                "threatType": "Port Scanning Detected",
                "port": str(port),
                "severity": "HIGH"
            })
            port_scan_tracker[src_ip] = set()

        # Check 3 - Brute Force Detection
        key = f"{src_ip}:{port}"
        if key not in brute_force_tracker:
            brute_force_tracker[key] = 0
        brute_force_tracker[key] += 1

        if brute_force_tracker[key] > 3:
            send_alert({
                "sourceIp": src_ip,
                "threatType": "Brute Force Attempt",
                "port": str(port),
                "severity": "CRITICAL"
            })
            brute_force_tracker[key] = 0

sniff(prn=analyze_packet, count=50)
print("\n✅ Capture Complete!")
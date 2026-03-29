from scapy.all import sniff, IP, TCP, UDP

print("🛡️ NIDS Started - Monitoring Network Traffic...")
print("Press Ctrl+C to stop\n")

def analyze_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        if TCP in packet:
            protocol = "TCP"
            port = packet[TCP].dport
        elif UDP in packet:
            protocol = "UDP"
            port = packet[UDP].dport
        else:
            protocol = "OTHER"
            port = 0
            
        print(f"From: {src_ip} → To: {dst_ip} | Protocol: {protocol} | Port: {port}")

# Capture 20 packets
sniff(prn=analyze_packet, count=20)

print("\n✅ Capture Complete!")
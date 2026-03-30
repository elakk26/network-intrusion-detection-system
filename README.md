# network-intrusion-detection-system
Real-time NIDS using Python, Spring Boot, React &amp; PostgreSQL
# Network Intrusion Detection System

Built this as a personal project to understand how network 
security tools work in real time. The idea came from my VAPT 
internship where I used Wireshark manually - so I wanted to 
automate that process.

## What it does

Monitors live network traffic on your machine, analyzes each 
packet, and flags suspicious activity like port scanning and 
brute force attempts. All alerts are stored in a database and 
displayed on a live dashboard.

## How it works

1. Python script captures live network packets using Scapy
2. Each packet is checked against threat detection rules
3. If suspicious - an alert is sent to Spring Boot API
4. Spring Boot saves the alert to PostgreSQL
5. React dashboard fetches and displays alerts every 5 seconds

## Tech Stack

- Python, Scapy, Npcap - packet capture and threat detection
- Java, Spring Boot - REST API backend
- PostgreSQL - stores all alerts
- React - live dashboard UI

## Threats Detected

- Port scanning
- Brute force attempts  
- Suspicious port access (SSH, Telnet, RDP, Metasploit)

## How to Run

Make sure PostgreSQL is running first

Start backend:
```
cd spring-boot-backend/nids-backend
mvn spring-boot:run
```

Run Python sniffer (open CMD as Administrator):
```
cd python-engine
python packet_sniffer.py
```

Start React dashboard:
```
cd react-frontend
npm start
```

Open browser at http://localhost:3000

## Screenshots
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/d989d27a-4d5b-4eef-a320-a82ae76d3918" />
<img width="956" height="1028" alt="image" src="https://github.com/user-attachments/assets/0a7b9a95-ffc5-4c19-b4fc-b820987f550c" />

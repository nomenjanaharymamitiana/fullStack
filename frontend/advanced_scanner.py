#!/usr/bin/env python3
import socket
import time
import threading

class AdvancedScanner:
    def __init__(self, target):
        self.target = target
    
    def full_port_scan(self, start_port=1, end_port=65535, timeout=2):
        """Comprehensive port scan"""
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((self.target, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(f"Port {port} is open")
            except:
                pass
        
        print(f"Scanning {self.target} from port {start_port} to {end_port}...")
        
        # Use threading for faster scanning
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(port,))
            threads.append(thread)
            thread.start()
            
            # Limit concurrent threads
            if len(threads) >= 100:
                for t in threads:
                    t.join()
                threads = []
        
        # Wait for remaining threads
        for thread in threads:
            thread.join()
        
        return sorted(open_ports)
    
    def detect_web_service(self, port):
        """Detect if port is running web service"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.target, port))
            
            # Try different HTTP requests
            requests = [
                f"GET / HTTP/1.1\r\nHost: {self.target}\r\n\r\n",
                f"GET / HTTP/1.0\r\n\r\n",
                f"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
            ]
            
            for req in requests:
                sock.send(req.encode())
                response = sock.recv(4096).decode('utf-8', errors='ignore')
                if response and ('HTTP' in response or '<html' in response.lower()):
                    sock.close()
                    return True, response[:200]
            
            sock.close()
            return False, ""
        except:
            return False, ""

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 advanced_scanner.py <target_ip>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = AdvancedScanner(target)
    
    # Scan common CTF port ranges
    port_ranges = [
        (3000, 3010),
        (8000, 8010),
        (32460, 32480),
        (9000, 9010),
        (1337, 1340)
    ]
    
    for start, end in port_ranges:
        print(f"\n=== Scanning ports {start}-{end} ===")
        open_ports = scanner.full_port_scan(start, end, timeout=1)
        
        if open_ports:
            print(f"Found open ports: {open_ports}")
            for port in open_ports:
                is_web, response = scanner.detect_web_service(port)
                if is_web:
                    print(f"Port {port} appears to be a web service:")
                    print(f"Response preview: {response}")
        else:
            print("No open ports found in this range")

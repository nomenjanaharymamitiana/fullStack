#!/usr/bin/env python3
import socket
import telnetlib
import time

class ServiceChecker:
    def __init__(self, target):
        self.target = target
    
    def check_ssh(self, port=22):
        """Check SSH service"""
        try:
            tn = telnetlib.Telnet(self.target, port, timeout=5)
            response = tn.read_some().decode('utf-8', errors='ignore')
            tn.close()
            return {'service': 'SSH', 'port': port, 'banner': response.strip()}
        except Exception as e:
            return {'service': 'SSH', 'port': port, 'error': str(e)}
    
    def check_dns(self, port=53):
        """Check DNS service"""
        try:
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [self.target]
            resolver.timeout = 5
            result = resolver.resolve('google.com', 'A')
            return {'service': 'DNS', 'port': port, 'status': 'working', 'result': str(result[0])}
        except Exception as e:
            return {'service': 'DNS', 'port': port, 'error': str(e)}
    
    def check_http_raw(self, port=80):
        """Check HTTP service with raw socket"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.target, port))
            
            # Send basic HTTP request
            request = f"GET / HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
            sock.send(request.encode())
            
            response = sock.recv(4096).decode('utf-8', errors='ignore')
            sock.close()
            
            return {'service': 'HTTP', 'port': port, 'response': response[:500]}
        except Exception as e:
            return {'service': 'HTTP', 'port': port, 'error': str(e)}
    
    def check_service_banner(self, port):
        """Get service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, port))
            
            # Wait for banner
            time.sleep(1)
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            return {'port': port, 'banner': banner.strip()}
        except Exception as e:
            return {'port': port, 'error': str(e)}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 service_checker.py <target_ip>")
        sys.exit(1)
    
    target = sys.argv[1]
    checker = ServiceChecker(target)
    
    print("=== Service Information ===")
    
    # Check SSH
    ssh_info = checker.check_ssh()
    print(f"SSH (22): {ssh_info}")
    
    # Check DNS
    dns_info = checker.check_dns()
    print(f"DNS (53): {dns_info}")
    
    # Check HTTP with raw socket
    http_info = checker.check_http_raw()
    print(f"HTTP (80): {http_info}")
    
    # Check for banners on common ports
    print("\n=== Service Banners ===")
    for port in [22, 53, 80]:
        banner_info = checker.check_service_banner(port)
        print(f"Port {port}: {banner_info}")

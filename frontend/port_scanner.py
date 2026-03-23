#!/usr/bin/env python3
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    def __init__(self, target, timeout=3):
        self.target = target
        self.timeout = timeout
        self.open_ports = []
        self.filtered_ports = []
    
    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                return {'port': port, 'status': 'open'}
            else:
                return {'port': port, 'status': 'closed'}
        except socket.timeout:
            return {'port': port, 'status': 'filtered'}
        except Exception:
            return {'port': port, 'status': 'error'}
    
    def scan_ports(self, ports, max_threads=50):
        """Scan multiple ports concurrently"""
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_port, port) for port in ports]
            
            for future in futures:
                result = future.result()
                if result['status'] == 'open':
                    self.open_ports.append(result['port'])
                elif result['status'] == 'filtered':
                    self.filtered_ports.append(result['port'])
        
        return {
            'open_ports': self.open_ports,
            'filtered_ports': self.filtered_ports
        }
    
    def test_http_service(self, port):
        """Test if a port is running HTTP service"""
        try:
            import requests
            url = f"http://{self.target}:{port}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            return {
                'port': port,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_length': len(response.text),
                'content_preview': response.text[:200]
            }
        except Exception as e:
            return {'port': port, 'error': str(e)}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 port_scanner.py <target_ip>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = PortScanner(target)
    
    # Scan common web ports and some random ports
    common_ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443]
    ctf_ports = list(range(3000, 3010)) + list(range(8000, 8010)) + list(range(32460, 32480))
    all_ports = common_ports + ctf_ports
    
    print(f"Scanning {target} for open ports...")
    results = scanner.scan_ports(all_ports)
    
    print(f"\nOpen ports: {results['open_ports']}")
    print(f"Filtered ports: {results['filtered_ports']}")
    
    # Test HTTP services on open ports
    if results['open_ports']:
        print("\nTesting HTTP services on open ports:")
        for port in results['open_ports']:
            if port in [80, 443, 8080, 8443, 3000, 8000] or 3000 <= port <= 9000:
                result = scanner.test_http_service(port)
                print(f"\nPort {port}:")
                if 'error' not in result:
                    print(f"  Status: {result['status_code']}")
                    print(f"  Content-Length: {result['content_length']}")
                    print(f"  Preview: {result['content_preview']}")
                else:
                    print(f"  Error: {result['error']}")

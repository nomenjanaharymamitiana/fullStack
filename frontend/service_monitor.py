#!/usr/bin/env python3
import requests
import time
import socket
from datetime import datetime

class ServiceMonitor:
    def __init__(self, target):
        self.target = target
        self.base_url = f"http://{target}:32469"
        self.alternative_ports = [80, 3000, 8000, 8080, 9000, 1337, 32468, 32470]
    
    def check_port(self, port, timeout=3):
        """Check if a port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_http_service(self, port):
        """Check if port is running HTTP service"""
        try:
            url = f"http://{self.target}:{port}"
            response = requests.get(url, timeout=5)
            return {
                'port': port,
                'status_code': response.status_code,
                'content_length': len(response.text),
                'server': response.headers.get('Server', ''),
                'content_type': response.headers.get('Content-Type', '')
            }
        except Exception as e:
            return {'port': port, 'error': str(e)}
    
    def monitor_all_ports(self, interval=30):
        """Monitor all relevant ports"""
        print(f"🔍 Monitoring {self.target} for service availability...")
        print(f"Checking ports: {self.alternative_ports}")
        print("=" * 60)
        
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}] Checking ports...")
            
            active_services = []
            
            # Check original port
            if self.check_port(32469):
                print(f"🚀 ORIGINAL PORT 32469 IS OPEN!")
                service_info = self.check_http_service(32469)
                print(f"Service info: {service_info}")
                active_services.append(32469)
            
            # Check alternative ports
            for port in self.alternative_ports:
                if self.check_port(port):
                    print(f"✅ Port {port} is open")
                    service_info = self.check_http_service(port)
                    if 'error' not in service_info and service_info['status_code'] != 0:
                        print(f"🌐 HTTP service on port {port}: {service_info}")
                        active_services.append(port)
                else:
                    print(f"❌ Port {port} is closed")
            
            if active_services:
                print(f"\n🎯 ACTIVE SERVICES FOUND ON PORTS: {active_services}")
                print("You can now run: python3 flag_hunter.py http://95.216.124.220:<port>")
                
                # Auto-launch flag hunter if original port is up
                if 32469 in active_services:
                    print("🚀 Auto-launching flag hunter for original challenge...")
                    return True
            
            print(f"Waiting {interval} seconds before next check...")
            time.sleep(interval)
    
    def quick_check(self):
        """Quick check of all ports"""
        print("Quick port scan...")
        
        # Check original port
        if self.check_port(32469):
            print("🚀 ORIGINAL PORT 32469 IS OPEN!")
            return True
        
        # Check alternatives
        for port in self.alternative_ports:
            if self.check_port(port):
                print(f"✅ Port {port} is open")
                service_info = self.check_http_service(port)
                if 'error' not in service_info:
                    print(f"🌐 HTTP service detected on port {port}")
                    return True
        
        print("❌ No web services detected")
        return False

if __name__ == "__main__":
    import sys
    
    target = "95.216.124.220"
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    monitor = ServiceMonitor(target)
    
    if len(sys.argv) > 2 and sys.argv[2] == "--quick":
        monitor.quick_check()
    else:
        monitor.monitor_all_ports()

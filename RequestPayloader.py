import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class HTTPRequestHandler:
    def __init__(self, base_url, session_cookie=None):
        self.base_url = base_url
        self.session_cookie = session_cookie
        self.cookies = {'PHPSESSID': session_cookie, 'security': "low"} if session_cookie else {}

    def set_session_cookie(self, session_cookie):
        self.session_cookie = session_cookie
        self.cookies = {'PHPSESSID': session_cookie}

    def manipulate_url(self, param, new_value):
        # Parse the URL
        parsed_url = urlparse(self.base_url)
        # Parse the query parameters
        query_params = parse_qs(parsed_url.query)
        # Update the specific parameter
        if param in query_params:
            query_params[param] = new_value
        # Encode the query parameters back to a query string
        new_query_string = urlencode(query_params, doseq=True)
        # Construct the new URL
        new_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query_string,
            parsed_url.fragment
        ))
        # print(new_url)
        return new_url

    def send_request(self, param=None, new_value=None, method='GET', data=None):
        url = self.base_url
        if param and new_value:
            url = self.manipulate_url(param, new_value)

        if method.upper() == 'GET':
            response = requests.get(url, cookies=self.cookies)
        elif method.upper() == 'POST':
            response = requests.post(url, data=data, cookies=self.cookies)
        else:
            raise ValueError("Unsupported HTTP method")
        
        return response

# example usage
if __name__ == '__main__':
    base_url = "http://localhost/vulnerabilities/fi/?page=file1.php"
    session_cookie = "r0gb7ua840v3i1jmun8o2t2re3"

    handler = HTTPRequestHandler(base_url, session_cookie)
    
    # Manipulate 'id' parameter to '10'
    response = handler.send_request(param="page", new_value="file2.php")
    
    # Print the response
    print(response.status_code)
    print(response.text)


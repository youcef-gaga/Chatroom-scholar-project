import socket
from threading import Thread

# server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = " " # we will use this to separate the client name & message

# prompt user to enter a username
username = input("Enter a username: ")

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# send the username to the server
s.send(f"{username}{separator_token}".encode())

def receive_message():
    """
    This function keep listening for a message from the server
    """
    while True:
        try:
            # keep listening for a message from the server
            msg = s.recv(1024).decode()
            if msg:
                print(msg)
        except (ConnectionError, ConnectionAbortedError):
            # client disconnected
            print(f"[-] Disconnected from the server.")
            s.close()
            break


# start a new thread that listens for messages from the server
t = Thread(target=receive_message)
t.daemon = True
# start the thread
t.start()

while True:

    message = input("")
    if message == 'exit':
        break
    # send the message to the server with the username
    s.send(f"{username}{separator_token}{message}".encode())

# close the client socket
s.close()

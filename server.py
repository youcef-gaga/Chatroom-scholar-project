import socket
from threading import Thread

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = " " # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a dictionary to store client's username and socket
client_usernames = {}
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
            # split the message to get client username and message
            client_username, msg = msg.split(separator_token)
        except (ConnectionError, ConnectionAbortedError):
            # client disconnected
            # remove it from the set and dictionary
            print(f"[-] {client_usernames[cs]} disconnected.")
            client_sockets.remove(cs)
            del client_usernames[cs]
            break
        else:
            # construct the message to be broadcasted
            msg = f"{client_usernames[cs]}: {msg}"
            # iterate over all connected sockets
            for client_socket in client_sockets:
                # and send the message
                client_socket.send(msg.encode())

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # receive client's username
    client_username = client_socket.recv(1024).decode()
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # add the client's username to the dictionary
    client_usernames[client_socket] = client_username
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()

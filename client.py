import socket
import select
import errno
import sys

HEADER_LENGTH = 20

IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# we connect client socket to the specified IP address and port
client_socket.connect((IP, PORT))
# we set blocking to False
client_socket.setblocking(False)

# we encode for safety reasons
username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    message = ""
    # handle for if anyone is inputting anything at all
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            # if we didn't get any data for whatever reason
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")
    except IOError as e:
        # these are unknown errors we would see depending on the operating system when there are no more messages to be received
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue
    except Exception as e:
        print('General error', str(e))
        sys.exit()

import socket
import select
# select helps us manage multiple connections regardless of the OS

# amount of max length of characters allowed in one message/input at a time from one connection/computer
HEADER_LENGTH = 20
# this is our local IP meaning that we are setting up this computer as a server that anyone on the same WiFi connection can connect to
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this lets us reconnect if the current port is occupied, so we can just reconnect every time, so it avoid bind() exception: OSError: [Errno 48] Address already in use and we set it to 1 which means True
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

# socket is now started and layer of communication is created
server_socket.listen()

# we need to manage our list of clients, and so we have server_socket on it which initiates the connection basically and then we have client sockets in here which themsevles initiate the connection
sockets_list = [server_socket]

clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        # if we didn't get any data, then the client closed the connection
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header" : message_header, "data" : client_socket.recv(message_length)}
    except:
        # this is just an exception handling for some client error
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # this means someone just connected
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)

            if message is False:
                print("Closed connection from {clients[notified_socket]['data'].decode('utf-8'')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]

            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

import socket
import time
import pickle

# we use pickle as a serialization and data transfer technique to transmit objects from one computer to another through the socket

# this example is how we handle inputs bigger than the buffer size, and it repeatedly accepts the message as a cycle

'''
a header is how our program knows how long the message is gonna be, and it's like ok once I have a message that length of 25, BOOM,
and technically, we create that message of length 25 because we wanted a fix input length to we added spaces to the message until
it is of length 25 and that is our fixed input that we see and is sent from the server to the client and that's how I know that message is done,
so now, I'm going to be waiting for another message again that is at most the size of the header, and once we reach that size, then boom that message is done, and we are now
onto the new message, and etc. the cycle repeats
'''
HEADERSIZE = 25

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostname())
# we bind out socket to a specific IP and port on the server
s.bind((socket.gethostname(), 1235))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d)
    #print(msg)
    # msg is now in bytes format
    # remember :<20 is for text aligning to the left with 20 leading characters after whatever comes before :<20 so we get a fixed length input
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    # UTF-8 encoding better than ASCII for text representation because it's more holistic and includes more kinds of characters
    clientsocket.send(msg)
    # clientsocket.close() this is just cause we wanted to continue sending data and not stop just as an example
    '''
    while True:
        time.sleep(3)
        msg = f"The time is: {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg, "utf-8"))
    '''

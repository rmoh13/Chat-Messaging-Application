import socket
import pickle

HEADERSIZE = 25

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''
We use socket.gethostname() because it will connect to a server on the same computer and machine so the host name is the same,
but usuqlly if we wanted the client to be remote and have them connect to a separate machine and another computer as the server
, we would put in a local or public IP often times
'''

# this example is how we handle inputs bigger than the buffer size, and it repeatedly accepts the message as a cycle

'''
a header is how our program knows how long the message is gonna be, and it's like ok once I have a message that size of 25, BOOM, that's how I know that message is done,
so now, I'm going to be waiting for another message again that is at most the size of the header, and once we reach that size, then boom that message is done, and we are now
onto the new message, and etc. the cycle repeats
'''

s.connect((socket.gethostname(), 1235))

while True:
    # this is our filter or buffer to receive 1024 bytes at a time, but a bit small
    full_msg = b""
    new_msg = True
    while True:
        # we just want to accept a stream of data, and this is useful if you want to restrict the input size and not send everything at once, and this is useful when you have characteer limits on the input for example
        # this receives a maxiumum of 32 bytes at a time in one input
        msg = s.recv(32)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            print("ful msg recvd")
            print(full_msg[HEADERSIZE:])

            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            new_msg = True
            full_msg = b""
        # now we decode the bytes we get
    print(full_msg)

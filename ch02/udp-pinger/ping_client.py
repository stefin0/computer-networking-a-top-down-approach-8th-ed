"""
You need to implement the following client program.
The client should send 10 pings to the server. Because UDP is an unreliable
protocol, a packet sent from the client to the server may be lost in the network,
or vice versa. For this reason, the client cannot wait indefinitely for a reply
to a ping message. You should get the client wait up to one second for a reply;
if no reply is received within one second, your client program should assume
that the packet was lost during transmission across the network. You will need
to look up the Python documentation to find out how to set the timeout value on
a datagram socket.

Specifically, your client program should
(1) send the ping message using UDP (Note: Unlike TCP, you do not need to
    establish a connection first, since UDP is a connectionless protocol.)
(2) print the response message from server, if any
(3) calculate and print the round trip time (RTT), in seconds, of each packet,
    if server responses
(4) otherwise, print “Request timed out”

During development, you should run the UDPPingerServer.py on your machine, and
test your client by sending packets to localhost (or, 127.0.0.1). After you have
fully debugged your code, you should see how your application communicates
across the network with the ping server and ping client running on different
machines.
"""

import socket
import time

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

for i in range(10):
    message = f"({i+1}) hello from client"
    client_socket.sendto(message.encode(), ("localhost", 12000))
    try:
        start_time = time.perf_counter()
        modified_message, server_address = client_socket.recvfrom(2048)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"{modified_message.decode()} ({duration:.5f}s)")
    except Exception as e:
        print(f"Error: {e}")

client_socket.close()

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

"""
Currently, the program calculates the round-trip time for each packet and prints
it out individually. Modify this to correspond to the way the standard ping
program works. You will need to report the minimum, maximum, and average RTTs at
the end of all pings from the client. In addition, calculate the packet loss
rate (in percentage).
"""

import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.settimeout(1.0)

    packets_lost = 0
    packets_total = 10
    rtts = []

    print(f"Pinging localhost:12000 with {packets_total} packets:")

    for i in range(1, packets_total + 1):
        message = f"Ping {i} {time.time()}"

        start_time = time.perf_counter()

        client_socket.sendto(message.encode(), ("localhost", 12000))

        try:
            modified_message, server_address = client_socket.recvfrom(2048)
            end_time = time.perf_counter()
            rtt = end_time - start_time
            rtts.append(rtt)
            print(f"Reply from {server_address}: seq={i} time={rtt*1000:.3f} ms")

        except socket.timeout:
            print(f"Request timed out for seq={i}")
            packets_lost += 1

    print(f"\n--- ping statistics ---")

    packets_received = packets_total - packets_lost
    packet_loss = (packets_lost / packets_total) * 100
    print(
        f"{packets_total} transmitted, {packets_received} received, {packet_loss:.1f}% packet loss"
    )

    if rtts:
        rtt_min = min(rtts) * 1000
        rtt_avg = (sum(rtts) / len(rtts)) * 1000
        rtt_max = max(rtts) * 1000
        print(f"rtt min/avg/max = {rtt_min:.3f}/{rtt_avg:.3f}/{rtt_max:.3f} ms")

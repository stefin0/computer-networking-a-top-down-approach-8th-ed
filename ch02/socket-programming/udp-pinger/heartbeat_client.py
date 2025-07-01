"""
2. Another similar application to the UDP Ping would be the UDP Heartbeat. The
Heartbeat can be used to check if an application is up and running and to report
one-way packet loss. The client sends a sequence number and current timestamp
in the UDP packet to the server, which is listening for the Heartbeat (i.e.,
the UDP packets) of the client. Upon receiving the packets, the server
calculates the time difference and reports any lost packets. If the Heartbeat
packets are missing for some specified period of time, we can assume that the
client application has stopped. Implement the UDP Heartbeat (both client and
server). You will need to modify the given UDPPingerServer.py, and your UDP
ping client.
"""

import socket
import time
import random

SERVER_PORT = 12000
SERVER_HOST = "localhost"
DROP_RATE = 0.5

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    seq = 0
    try:
        while True:
            rand = random.randint(0, 10)

            # 50% chance request is not sent
            if random.random() < DROP_RATE:
                print(f"Dropping packet {seq}")
            else:
                # Send sequence number and current timestamp
                request = f"{seq} {time.time()}"
                client_socket.sendto(request.encode(), (SERVER_HOST, SERVER_PORT))
                print(f"Sent heartbeat {seq}")

            seq += 1
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nClient is shutting down...")

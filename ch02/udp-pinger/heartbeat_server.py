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

SERVER_PORT = 12000
SERVER_HOST = "localhost"

# Create socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    # Socket options
    server_socket.settimeout(5.0)

    # Bind socket
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    print("The (heartbeat) server is ready to receive")

    last_seen_seq = 0
    try:
        while True:
            try:
                # Receive the client packet along with the address it is coming from
                request, client_address = server_socket.recvfrom(1024)
                message = request.decode()

                # calculates the time difference and reports any lost packets.
                parts = message.split()
                current_seq = int(parts[0])
                client_timestamp = float(parts[1])

                print(f"Received heartbeat {current_seq} from {client_address}.")

                if current_seq > last_seen_seq + 1:
                    lost_count = current_seq - (last_seen_seq + 1)
                    print(
                        f"   Detected {lost_count} lost packet(s). Expected sequence {last_seen_seq + 1}."
                    )

                time_diff_ms = (time.time() - client_timestamp) * 1000
                print(f"   One-way latency: {time_diff_ms:.3f} ms.")

                last_seen_seq = current_seq

            except TimeoutError:
                print("Client has no heartbeat")

    except KeyboardInterrupt:
        print("\nServer is shutting down...")

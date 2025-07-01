"""
2. Instead of using a browser, write your own HTTP client to test your server.
Your client will connect to the server using a TCP connection, send an HTTP
request to the server, and display the server response as an output. You can
assume that the HTTP request sent is a GET method. The client should take
command line arguments specifying the server IP address or host name, the port
at which the server is listening, and the path at which the requested object is
stored at the server. The following is an input command format to run the client.

client.py server_host server_port filename
"""

import socket
import sys

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 1. Connect to the server using a TCP connection
client_socket.connect((sys.argv[1], int(sys.argv[2])))

# 2. Send an HTTP request to the server
request_line = f"GET /{sys.argv[3]} HTTP/1.1\r\n"
header_lines = "Connection: close\r\n"

request = request_line + header_lines + "\r\n"

client_socket.send(request.encode())

response = b""
while True:
    data = client_socket.recv(2048)
    if not data:
        break
    response += data

# 3. Display the server response as output.
print(f"Resonse from server:\n{response.decode()}")

client_socket.close()

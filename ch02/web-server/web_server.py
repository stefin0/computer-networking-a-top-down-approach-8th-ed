"""
In this assignment, you will develop a simple Web server in Python that is
capable of processing only one request. Specifically, your Web server will (i)
create a connection socket when contacted by a client (browser); (ii) receive
the HTTP request from this connection; (iii) parse the request to determine the
specific file being requested; (iv) get the requested file from the server’s
file system; (v) create an HTTP response message consisting of the requested
file preceded by header lines; and (vi) send the response over the TCP
connection to the requesting browser. If a browser requests a file that is not
present in your server, your server should return a “404 Not Found” error
message.
"""

import socket
import sys

# Create a server socket.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the SO_REUSEADDR option.
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server socket.
serverPort = 6789
serverSocket.bind(("", serverPort))

serverSocket.listen(1)
print(f"Server is listening on port {serverPort}.")

while True:
    # Establish the connection.
    print("Ready to serve...\n")
    # (i) Create a connection socket when contacted by a client (browser)
    connectionSocket, addr = serverSocket.accept()

    try:
        # (ii) receive the HTTP request from the connection socket
        message = connectionSocket.recv(2048).decode()

        # (iii) parse the request to determine the specific file being
        #       requested
        filename = message.split()[1]

        # (iv) get the requested file from the server's file system
        f = open(filename[1:])
        entity_body = f.read()

        # (v) create an HTTP response message consisting of the requested file
        #     preceded by header lines
        status_line = "HTTP/1.1 200 OK\r\n"
        headers_list = [
            "Connection: close",
            f"Content-Length: {len(entity_body.encode())}",
            "Content-Type: text/html\r\n",
        ]
        headers = "\r\n".join(headers_list)
        blank_line = "\r\n"
        outputdata = [status_line, headers, blank_line, entity_body]

        # (vi) send the response over the TCP connection to the requesting
        #      browser.
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # If a browser requests a file that is not present in your server,
        # your server should return a “404 Not Found” error message.
        status_line = "HTTP/1.1 404 Not Found\r\n"
        headers_list = [
            "Connection: close",
        ]
        headers = "\r\n".join(headers_list)
        outputdata = [status_line, headers]
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data

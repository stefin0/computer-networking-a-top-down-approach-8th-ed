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

1. Currently, the web server handles only one HTTP request at a time. Implement
a multithreaded server that is capable of serving multiple requests
simultaneously. Using threading, first create a main thread in which your
modified server listens for clients at a fixed port. When it receives a TCP
connection request from a client, it will set up the TCP connection through
another port and services the client request in a separate thread. There will
be a separate TCP connection in a separate thread for each request/response pair.
"""

import socket
import sys
import time
import threading

SERVER_HOST = "localhost"
SERVER_PORT = 6789


def client_handler(connection_socket, addr):
    """Handles the request from a single client in a dedicated thread."""
    print(
        f"Accepted connection from {addr}. Servicing in thread {threading.current_thread().name}"
    )
    try:
        # (ii) receive the HTTP request from the connection socket
        time.sleep(0.05)
        request = connection_socket.recv(2048).decode("utf-8")

        # if the request is empty (e.g., client disconnected), skip
        if not request:
            connection_socket.close()
            return

        # (iii) parse the request to determine the specific file being
        #       requested
        try:
            filename = request.split()[1]
        except IndexError:
            print("Malformed request received.")
            connection_socket.close()
            return

        # (iv) get the requested file from the server's file system
        try:
            with open(filename.lstrip("/"), "r") as file:
                file_content = file.read()

            # (v) create an HTTP response message consisting of the
            #     requested file preceded by header lines
            status_line = "HTTP/1.1 200 OK\r\n"
            headers = "Content-Type: text/html; charset=utf-8\r\n"
            headers += f"Content-Length: {len(file_content.encode("utf-8"))}\r\n"
            response = status_line + headers + "\r\n" + file_content

        except FileNotFoundError:
            # (vi) if a browser requests a file that is not present in the
            #      server, the server should return a “404 Not Found”
            #      error message.
            print(f"File not found: {filename}")
            status_line = "HTTP/1.1 404 Not Found\r\n"
            headers = "Content-Type: text/html; charset=utf-8\r\n"
            response = status_line + headers + "\r\n"

        # (vi) send the response over the TCP connection to the requesting
        #      browser.
        connection_socket.sendall(response.encode("utf-8"))

    except Exception as e:
        print(f"Error handling request: {e}")

    finally:
        connection_socket.close()


def main():
    """Main function to set up and run the multithreaded server."""
    # create the server socket.
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as error:
        print(f"Error creating socket: {error}")
        sys.exit(1)

    # bind the server socket.
    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
    except socket.error as error:
        print(f"Error binding socket to port {SERVER_PORT}: {error}")
        sys.exit(1)

    server_socket.listen(5)
    print(f"Server is listening on http://{SERVER_HOST}:{SERVER_PORT}.")

    try:
        while True:
            # (i) create a connection socket when contacted by a client (browser)
            connection_socket, addr = server_socket.accept()

            # Create a new thread to handle the client request.
            client_thread = threading.Thread(
                target=client_handler, args=(connection_socket, addr), daemon=True
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer is shutting down.")

    except Exception as e:
        print(f"An unexpected error occured in the server loop: {e}")

    finally:
        server_socket.close()
        print("Server socket closed.")
        sys.exit()


if __name__ == "__main__":
    main()

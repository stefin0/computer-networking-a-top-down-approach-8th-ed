import base64
import os
import socket
import ssl
import sys

import dotenv

dotenv.load_dotenv()

USERNAME = os.getenv("USERNAME")
if not USERNAME:
    print("Error: USERNAME environment variable not found.")
    print("Please set it in your .env file.")
    sys.exit(1)

GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
if not GMAIL_APP_PASSWORD:
    print("Error: GMAIL_APP_PASSWORD environment variable not found.")
    print("Please set it in your .env file.")
    sys.exit(1)

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
MAILSERVER_NAME = "smtp.gmail.com"
MAILSERVER_PORT = 465

context = ssl.create_default_context()

# Create socket called client_socket and establish a TCP connection with mailserver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Wrap socket to handle TLS encryption
    with context.wrap_socket(
        client_socket, server_hostname=MAILSERVER_NAME
    ) as s_client_socket:
        try:
            s_client_socket.connect((MAILSERVER_NAME, MAILSERVER_PORT))
        except Exception as e:
            print(f"connect: {e}")
        response = s_client_socket.recv(1024).decode()
        print(response)
        if response[:3] != "220":
            print("220 reply not received from server.")

        # Send HELO command and print server response.
        ehlo_command = f"EHLO stefin\r\n"
        s_client_socket.send(ehlo_command.encode())
        response = s_client_socket.recv(1024).decode()
        print(response)

        # Send AUTH LOGIN command and print server response
        authlogin_command = "AUTH LOGIN\r\n"
        s_client_socket.send(authlogin_command.encode())
        response = s_client_socket.recv(2048).decode()
        print(response)

        # Send Username and print server response
        username_message = base64.b64encode(USERNAME.encode()) + b"\r\n"
        s_client_socket.send(username_message)
        response = s_client_socket.recv(2048).decode()
        print(response)

        # Send Password and print server response
        password_message = base64.b64encode(GMAIL_APP_PASSWORD.encode()) + b"\r\n"
        s_client_socket.send(password_message)
        response = s_client_socket.recv(2048).decode()
        print(response)

        # Send MAIL FROM command and print server response.
        # mail_from_command = f"MAIL FROM: <{username}>\r\n"
        # client_socket.send(mail_from_command.encode())
        # recv2 = client_socket.recv(1024).decode()
        # print(recv2)
        #
        # # Send RCPT TO command and print server response.
        # rcpt_to_command = "RCPT TO: <stefinracho@gmail.com>\r\n"
        # client_socket.send(rcpt_to_command.encode())
        # recv3 = client_socket.recv(1024).decode()
        # print(recv3)
        #
        # # Send DATA command and print server response.
        # data_command = "DATA\r\n"
        # client_socket.send(data_command.encode())
        # recv4 = client_socket.recv(1024).decode()
        # print(recv4)
        #
        # # Send message data.
        # client_socket.send(msg.encode())
        #
        # # Message ends with a single period.
        # client_socket.send(endmsg.encode())
        #
        # # Send QUIT command and get server response.
        # quit_command = "QUIT\r\n"
        # client_socket.send(quit_command.encode())
        # recv5 = client_socket.recv(1024).decode()
        # print(recv5)

import base64
import os
import socket
import ssl
import sys

import dotenv

dotenv.load_dotenv()

MAILSERVER_HOST = "smtp.gmail.com"
MAILSERVER_PORT = 465
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"


def check_env_vars():
    """Checks for required environment variables and exits if they are missing."""
    if not SENDER_EMAIL:
        print("Error: USERNAME environment variable not found.", file=sys.stderr)
        print("Please set it in your .env file.", file=sys.stderr)
        sys.exit(1)
    if not GMAIL_APP_PASSWORD:
        print(
            "Error: GMAIL_APP_PASSWORD environment variable not found.", file=sys.stderr
        )
        print("Please set it in your .env file.", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to connect, authenticate, and send an email."""
    check_env_vars()

    context = ssl.create_default_context()

    # Create socket called client_socket and establish a TCP connection with mailserver
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_client_socket:
        # Wrap socket to handle TLS encryption
        with context.wrap_socket(
            s_client_socket, server_hostname=MAILSERVER_HOST
        ) as s_client_socket:
            try:
                s_client_socket.connect((MAILSERVER_HOST, MAILSERVER_PORT))
            except Exception as e:
                print(f"connect: {e}")
            response = s_client_socket.recv(1024).decode()
            print(response)
            if response[:3] != "220":
                print("220 reply not received from server.")

            # Send HELO command and print server response.
            ehlo_command = f"EHLO stefin\r\n"
            s_client_socket.sendall(ehlo_command.encode())
            response = s_client_socket.recv(1024).decode()
            print(response)

            # Send AUTH LOGIN command and print server response
            authlogin_command = "AUTH LOGIN\r\n"
            s_client_socket.sendall(authlogin_command.encode())
            response = s_client_socket.recv(2048).decode()
            print(response)

            # Send Username and print server response
            username_message = base64.b64encode(SENDER_EMAIL.encode()) + b"\r\n"
            s_client_socket.sendall(username_message)
            response = s_client_socket.recv(2048).decode()
            print(response)

            # Send Password and print server response
            password_message = base64.b64encode(GMAIL_APP_PASSWORD.encode()) + b"\r\n"
            s_client_socket.sendall(password_message)
            response = s_client_socket.recv(2048).decode()
            print(response)

            # Send MAIL FROM command and print server response.
            mail_from_command = f"MAIL FROM: <{SENDER_EMAIL}>\r\n"
            s_client_socket.sendall(mail_from_command.encode())
            response = s_client_socket.recv(1024).decode()
            print(response)

            # Send RCPT TO command and print server response.
            rcpt_to_command = f"RCPT TO: <{SENDER_EMAIL}>\r\n"
            s_client_socket.sendall(rcpt_to_command.encode())
            response = s_client_socket.recv(1024).decode()
            print(response)

            # Send DATA command and print server response.
            data_command = "DATA\r\n"
            s_client_socket.sendall(data_command.encode())
            response = s_client_socket.recv(1024).decode()
            print(response)

            # Send message data.
            s_client_socket.sendall(msg.encode())

            # Message ends with a single period.
            s_client_socket.sendall(endmsg.encode())

            # Send QUIT command and get server response.
            quit_command = "QUIT\r\n"
            s_client_socket.sendall(quit_command.encode())
            response = s_client_socket.recv(1024).decode()
            print(response)


if __name__ == "__main__":
    main()

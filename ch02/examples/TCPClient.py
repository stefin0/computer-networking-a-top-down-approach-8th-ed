from socket import *

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input("Input lowercase sentence (-1 to quit): ")
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(2048)
print("From Server: ", modifiedSentence.decode())

clientSocket.close()

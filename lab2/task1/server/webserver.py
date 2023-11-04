from socket import *
serverPort = 11000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("127.0.0.1", serverPort))
serverSocket.listen(1)
print ("The server is ready to receive")
while True:
    # Write http://127.0.0.1:11000/HelloWorld.html on web browser
    # Server will detect the request and print the addr from client
    connectionSocket, addr = serverSocket.accept()
    if addr:
        print("Connection from: ", addr)
    break
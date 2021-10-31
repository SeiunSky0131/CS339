from socket import *
import time

serverPort = 2680
buffersize = 2048 #define the buffer size for message receiving

serverSocket = socket(AF_INET,SOCK_STREAM) #create a TCP socket for the server
serverSocket.bind(('',serverPort)) #bind the port to the socket, this means the socket is attached to the server

#Let's assume that the socket can communicate with 5 clients at the same time
serverSocket.listen(1)
print('server initialized')
#define a universal variable for the number of clients connected
num_of_clients = 0

while True:
    #then the server will be ready to accept connection information
    #the accept function return a new sokcet for a particular connection
    #and the address of the client
    connectionSocket, addr = serverSocket.accept()

    #prepare the client number for that client and send to the corresponding address
    num_of_clients = num_of_clients + 1
    client_num = '%d'%num_of_clients
    connectionSocket.sendall(client_num,addr)

    time.sleep(1) #stop for some time and then start sending file
    
    fs = open('test.txt')
    print('The server now begins to send the file to: ', addr)

    while True:
        #read in the file content to buffer
        buffer = fs.read(buffersize)

        #if the buffer no longer get message, then the file ends
        if not buffer:
            break
        connectionSocket.sendall(buffer.encode())
    connectionSocket.sendall(''.encode())
    #close the opened file
    fs.close()

    print("the file has already sent to: ", addr)
    #close this particular connection with the client
    connectionSocket.close()

    #now the loop goes for another conection
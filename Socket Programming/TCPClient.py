from socket import *
import time


serverName = '10.0.0.1'
serverPort = 2680
buffersize = 2048 #define the buffer size for message receiving
Addr = (serverName,serverPort) #can be regraded as the IP address
clientSocket = socket(AF_INET,SOCK_STREAM) #create a TCP socket
clientSocket.connect(Addr) #connect the socket to the port

#send the message to the server for first handshake
clientSocket.sendall("nice!".encode())

#EFFECT: get and return the client number from the socket
def get_client_number():
    client_number = clientSocket.recv(buffersize).decode()
    clinet_number_int = int(client_number)
    return clinet_number_int

#EFFECT: create the file corresponding to the client number in the client
#        return the opened file
def create_file(client_number_int):
    filename = 'file%d.txt'%client_number_int
    opened_file = open(filename,'wb')
    return opened_file

#then the client is ready to get message into the file
client_num = get_client_number()
fs = create_file(client_num)
time.sleep(0.5)

start = time.time() #start the clock
print('client %d begins to receive the file'%client_num)
while True:
    buffer = clientSocket.recv(buffersize) #create a new buffer to receive the file
    if not len(buffer): #if the buffer receives an empty string sent by server, it terminates
        break
    fs.write(buffer)

fs.flush()
fs.close()
end = time.time() #stop the clock
print('the file is already received by client %d, the time used is %d seconds'%(client_num,end-start))

#close the socket
clientSocket.close()




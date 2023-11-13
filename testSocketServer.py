from socket import *

serverName = 'localhost'
serverPort = 9000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)

print('Server is ready to receive...')

while True:
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr)

    # Receive data from NUGU Server
    data = b''
    while True:
        chunk = connectionSocket.recv(1024)
        if not chunk:
            break
        data += chunk
        if b'\n' in chunk:
            break  # Break the loop when newline character is received

    # Print recieved data from NUGU Server
    received_data = data.decode().strip()
    print('Received from client:', received_data)
    connectionSocket.close()
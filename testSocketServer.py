import socket
import threading
import json

frontend_server_address = ('localhost', 9000)

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        json_data = json.loads(data)
        print("Received data from Flask server:", json_data)

    except Exception as e:
        print("Error handling client:", str(e))
    finally:
        client_socket.close()

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(frontend_server_address)
        server_socket.listen()

        print(f"TCP server listening on {frontend_server_address}")

        while True:
            client_socket, _ = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == '__main__':
    start_tcp_server()
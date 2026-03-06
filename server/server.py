import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server running on {HOST}:{PORT}")

while True:
    client_socket, address = server_socket.accept()
    print(f"Client connected from {address}")
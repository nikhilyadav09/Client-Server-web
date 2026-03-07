import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server running on {HOST}:{PORT}")

clients = []


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def handle_client(client_socket, address):

    print(f"New connection from {address}")

    clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode()

            print(f"[{address}] {message}")

            broadcast(data, client_socket)

        except:
            break

    print(f"Client disconnected: {address}")

    clients.remove(client_socket)

    client_socket.close()


while True:

    client_socket, address = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )

    thread.start()
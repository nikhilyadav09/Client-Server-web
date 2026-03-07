import socket
import threading
from datetime import datetime

LOG_FILE = "chat.log"

open(LOG_FILE, "a").close()

def log_event(message):
    """Write chat events to log file."""
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def get_recent_history(limit=20):
    """Return the last 'limit' lines from the chat log."""
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            return lines[-limit:]
    except FileNotFoundError:
        return []
    
HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server running on {HOST}:{PORT}")

clients = {}
lock = threading.Lock()


def broadcast(message, sender_socket=None):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    clients.pop(client, None)


def handle_client(client_socket, address):

    try:
        username = client_socket.recv(1024).decode()

        # send recent chat history to the newly connected client
        history = get_recent_history()

        if history:
            client_socket.send("---- Recent Chat History ----\n".encode())
            for line in history:
                client_socket.send(line.encode())
            client_socket.send("-----------------------------\n".encode())

        with lock:
            clients[client_socket] = username

        print(f"{username} joined from {address}")

        timestamp = datetime.now().strftime("%H:%M:%S")
        join_msg = f"[{timestamp}] {username} joined the chat"

        print(join_msg)

        broadcast(join_msg)

        log_event(join_msg)

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode()

            # client requested quit
            if message.strip() == "QUIT":
                break

            # command: /users
            if message.strip() == "/users":

                with lock:
                    user_list = ", ".join(clients.values())

                timestamp = datetime.now().strftime("%H:%M:%S")

                response = f"[{timestamp}] Online users: {user_list}"

                client_socket.send(response.encode())

                log_event(response)

                continue


            timestamp = datetime.now().strftime("%H:%M:%S")

            full_message = f"[{timestamp}] {username}: {message}"

            print(full_message)

            broadcast(full_message, client_socket)

            log_event(full_message)

    except:
        pass

    finally:

        with lock:
            username = clients.get(client_socket, "Unknown")
            clients.pop(client_socket, None)

        print(f"{username} left the chat")

        timestamp = datetime.now().strftime("%H:%M:%S")

        leave_msg = f"[{timestamp}] {username} left the chat"

        print(leave_msg)

        broadcast(leave_msg)

        log_event(leave_msg)

        client_socket.close()


while True:

    client_socket, address = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )

    thread.start()
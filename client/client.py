import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print("Connected to chat server")


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            print(message)

        except:
            print("Connection closed.")
            break


def send_messages():
    while True:
        message = input()

        if message.lower() == "/quit":
            client_socket.close()
            break

        client_socket.send(message.encode())


receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()
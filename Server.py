import socket
import threading

def broadcast(message, sender_name):
    for client in clients:
        try:
            if client["name"] != sender_name:
                client["socket"].send(f'{sender_name}: {message}'.encode())
        except BrokenPipeError:
            continue

def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except ConnectionResetError:
            message = None

        if not message:
            index = next((i for i, c in enumerate(clients) if c["socket"] == client_socket), None)
            if index is not None:
                client = clients.pop(index)
                client_socket.close()
                broadcast('has left the chat room', client["name"])
            break

        print(f"Received from {client_name}: {message}")
        broadcast(message, client_name)

server_ip = "localhost"
server_port = 12348

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)
clients = []

print(f"Server listening on {server_ip}:{server_port}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Get a unique name from the user
    client_name = client_socket.recv(1024).decode()

    # Start a new thread to handle the client
    clients.append({"socket": client_socket, "name": client_name})
    broadcast('has joined the chat room', client_name)
    client_socket.send('You are now connected!'.encode())
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
    client_handler.start()

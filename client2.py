import socket
import threading
import time

def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode()
            print(response)
        except ConnectionAbortedError:
            print("Connection to the server closed.")
            break

def send_messages(client_socket, client_name):
    while True:
        message = input("")
        client_socket.send(f"{message}".encode())

# Server IP and port
server_ip = "localhost"
server_port = 12348

# Get a unique name from the user
client_name = input("Enter your unique name: ")

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Send the client name to the server
client_socket.send(client_name.encode())

# Start threads for sending and receiving messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_messages, args=(client_socket, client_name))

receive_thread.start()
send_thread.start()

# Wait for the sending thread to finish (receiving thread will continue running)
send_thread.join()

# Close the client socket when done
client_socket.close()

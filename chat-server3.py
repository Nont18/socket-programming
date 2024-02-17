import socket
import threading
import sys

PORT = 7500
BUFSIZE = 4096
SERVERIP = 'localhost'

# Use a lock for thread-safe access to the client list
client_list_lock = threading.Lock()
clist = []  # client list

def broadcast(message, sender_client):
    with client_list_lock:
        for client in clist:
            # Send the message to all clients except the sender
            if client != sender_client:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting message: {e}")

def client_handler(client, addr):
    try:
        # Receive username from the client
        username = client.recv(BUFSIZE).decode('utf-8')
        with client_list_lock:
            clist.append(client)
        print(f"{username} has joined the chat.")

        # Broadcast the join message to all clients
        broadcast(f"chat:{username} has joined the chat.", client)

        while True:
            data = client.recv(BUFSIZE).decode('utf-8')
            if not data:
                break

            if data == 'q':
                # Handle client leaving the chat
                with client_list_lock:
                    clist.remove(client)
                broadcast(f"chat:{username} has left the chat.", client)
                break

            # Broadcast regular chat message
            broadcast(f"chat:{username}:{data}", client)

    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
        client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((SERVERIP, PORT))
    server.listen(5)
    print(f"Server listening on {SERVERIP}:{PORT}")

    while True:
        client, addr = server.accept()
        with client_list_lock:
            clist.append(client)
        print('ALL CLIENTS: ', clist)

        # Send a welcome message to the client
        client.sendall("Welcome to the chat! Enter your username:".encode('utf-8'))

        task = threading.Thread(target=client_handler, args=(client, addr))
        task.start()

except Exception as e:
    print(f"Error in server setup: {e}")

finally:
    server.close()

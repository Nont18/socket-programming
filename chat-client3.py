import socket
import threading
import sys

PORT = 7500
BUFSIZE = 4096
SERVERIP = 'localhost'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    client.connect((SERVERIP, PORT))
except socket.error as e:
    print(f'Error connecting to the server: {e}')
    sys.exit()

# Receive the welcome message from the server
welcome_message = client.recv(BUFSIZE).decode('utf-8')
print(welcome_message)

username = input("Enter your username: ")
client.sendall(username.encode('utf-8'))

def receive_messages():
    while True:
        try:
            data = client.recv(BUFSIZE).decode('utf-8')
            print(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

try:
    while True:
        msg = input('Message: ')
        client.sendall(msg.encode('utf-8'))
        if msg == 'q':
            break
except KeyboardInterrupt:
    print('User interrupted. Closing the client.')

finally:
    client.close()

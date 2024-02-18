import socket
import datetime
import threading

PORT = 7500
BUFSIZE = 4096
SERVERIP = '192.168.1.38' #your ip

client_list_lock = threading.Lock()
clist = [] #client list


def broadcast(message, sender_client):
    with client_list_lock:
        for client in clist:
            # Send the message to all clients except the sender
            if client != sender_client:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting message: {e}")

def client_handler(client,addr):
    while True:
        try:
            data = client.recv(BUFSIZE)
        except:
            clist.remove(client)
            break
        
        if (not data) or (data.decode('utf-8') == 'q'):
            clist.remove(client)
            print('OUT : ', client)
            break
        msg = str(addr) + '>>> ' + data.decode('utf-8')
        client.sendall(msg.encode('utf-8'))
        broadcast(msg, client) #boardcast this message to everyone in chat room
        print('USER: ', msg)
        print('-----------')
        
    client.close()
    
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #use TCP
server.bind((SERVERIP, PORT))
server.listen(5)

while True:
    client, addr = server.accept()
    clist.append(client)
    print('ALL CLIENT: ', clist)
    task = threading.Thread(target=client_handler, args=(client, addr))
    task.start()
    


    
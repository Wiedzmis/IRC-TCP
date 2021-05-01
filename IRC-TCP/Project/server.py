import threading
import socket

host = "127.0.0.1" #localhost | Albo serwera
port = 21376

clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = socket | SOCK_STREAM = TCP
server.bind((host, port)) 
server.listen() #nasłuchuje nowe połączenia

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except: #Jeżeli sie nie uda to usuń klienta z list i odrzuć połączenie
            index = clients.index(client) #zdobywam index(id) klienta
            clients.remove(client) # usuwamy klienta
            client.close() #zamykamy z klientem połączenie
            nickname = nicknames[index] #za pomocą indexu pozyskujemy jego nick
            broadcast(f'{nickname} had to leave'.encode('ascii')) #nadajemy do wszystkich klientów wiadomości broadcastem
            nicknames.remove(nickname) #usuwamy klienta z listy
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Someone is connecting from {str(address)}")

        client.send('NICK'.encode('ascii')) # wysyłamy słowo kluczowe do klienta
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'His nickname is {nickname}')
        broadcast(f'{nickname} arrives!') #nadajemy do wszystkich klientów wiadomości broadcastem
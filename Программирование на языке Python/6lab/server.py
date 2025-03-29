import socket
import threading

clients = [] #сокеты подключения всех клиентов

def serve_client(client, client_num):
    msg = "Добро пожаловать, клиент #" + str(client_num) + "!"
    for i in range(len(msg) + 1, 1024 + 1):
        msg += '\0'
    client.send(msg.encode())
    message = ""
    while True:
        try:
            while len(message) < 1024:
                message += client.recv(1024).decode()
            msg = ""
            for i in range(len(message)):
                if message[i] == '\0':
                    break
                msg += message[i]
            msg = msg.upper()
            msg = "Клиент #" + str(client_num) + ": " + msg
            print(msg)
            for i in range(len(msg)+1, 1024+1):
                msg += '\0'
            for c in clients:
                c.send(msg.encode())
            message = ""
        except:
            clients.remove(client)
            print("Соединение с клиентом потеряно")
            return


def serve():
    cnum = 1
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 3333))
    print("Начал работу")
    while True:
        server.listen(3)
        if len(clients) >= 3:
            continue
        client_socket, client_addr = server.accept()
        print("Клиент зашёл")
        clients.append(client_socket)
        thread = threading.Thread(target=serve_client, args=[client_socket, cnum])
        thread.start()
        cnum += 1
serve()

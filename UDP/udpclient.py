import socket
import threading
import os

# Variável global para armazenar o nickname do usuário
user_nickname = None

def receive_messages(client_socket):
    while True:
        try:
            data, _ = client_socket.recvfrom(2048)
            print(data.decode('utf-8'))
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            break

def send_message(client_socket, server_address, message):
    client_socket.sendto(message.encode('utf-8'), server_address)

def send_file(client_socket, server_address, command):
    parts = command.split()
    if len(parts) >= 3:
        file_path = parts[2]
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                header = f'/SEND {os.path.basename(file_path)}'.encode('utf-8')
                client_socket.sendto(header + b' ' + file_data, server_address)
        except FileNotFoundError:
            print("Arquivo não encontrado.")

def handle_user_input(client_socket, server_address):
    while True:
        message = input("-> ")
        send_message(client_socket, server_address, message)

def register_user(client_socket, server_address):
    global user_nickname
    nickname = input("Digite seu apelido para registro: ")
    if nickname:
        user_nickname = nickname
        send_message(client_socket, server_address, f"/REG {nickname}")

def main():
    server_host = '127.0.0.1'
    server_port = 5555
    server_address = (server_host, server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        register_user(client_socket, server_address)
        threading.Thread(target=receive_messages, args=(client_socket,)).start()
        handle_user_input(client_socket, server_address)
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        client_socket.close()

if __name__ == "__main__":
    main()

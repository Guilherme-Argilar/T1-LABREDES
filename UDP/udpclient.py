import socket
import threading
import os

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
    client_socket.sendto(f"{user_nickname}: {message}".encode('utf-8'), server_address)

def send_private_message(client_socket, server_address, recipient, message):
    formatted_message = f"/MSG {recipient} {message}"
    client_socket.sendto(formatted_message.encode('utf-8'), server_address)

def send_file(client_socket, server_address, command):
    parts = command.split()
    if len(parts) >= 3:
        file_path = parts[2]
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                file_size = len(file_data)
                header = f'/FILE {user_nickname} {os.path.basename(file_path)} {file_size}'.encode('utf-8')
                print(f"Enviando cabeçalho: {header}")
                client_socket.sendto(header, server_address)
                client_socket.sendto(file_data, server_address)
                print(f"Enviando dados do arquivo de tamanho {file_size} bytes")
        except FileNotFoundError:
            print("Arquivo não encontrado.")


def list_users(client_socket, server_address):
    client_socket.sendto("/LIST".encode('utf-8'), server_address)

def process_command(client_socket, server_address, command):
    if command.startswith("/MSG") and len(command.split()) > 2:
        parts = command.split(' ', 2)
        send_private_message(client_socket, server_address, parts[1], parts[2])
    elif command.startswith("/SEND"):
        send_file(client_socket, server_address, command)
    elif command.startswith("/LIST"):
        list_users(client_socket, server_address)
    elif command.startswith("/S"):
        send_message(client_socket, server_address, command)

def handle_user_input(client_socket, server_address):
    while True:
        message = input("-> ")
        if message.startswith("/"):
            process_command(client_socket, server_address, message)
        else:
            print('comando desconhecido')

def register_user(client_socket, server_address):
    global user_nickname
    nickname = input("Digite seu apelido para registro: ")
    if nickname:
        user_nickname = nickname
        client_socket.sendto(f"/REG {nickname}".encode('utf-8'), server_address)

def main():
    server_host = '127.0.0.1'
    server_port = 5555
    server_address = (server_host, server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    register_user(client_socket, server_address)
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    handle_user_input(client_socket, server_address)

if __name__ == "__main__":
    main()

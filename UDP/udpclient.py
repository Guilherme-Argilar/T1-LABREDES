import socket
import threading
import os

user_nickname = None
is_running = True
def receive_messages(client_socket):
    global is_running
    while is_running:
        try:
            data, _ = client_socket.recvfrom(2048)
            if data:
                if data.startswith(b"/FILE"):
                    header_parts = data.decode('utf-8').split()
                    filename = header_parts[1]
                    file_size = int(header_parts[2])
                    file_data, _ = client_socket.recvfrom(file_size)
                    with open(filename, "wb") as f:
                        f.write(file_data)
                    print(f"Arquivo recebido com sucesso: {filename}")
                else:
                    print(data.decode('utf-8'))
        except Exception as e:
            if is_running:
                print(f"Erro ao receber dados: {e}")
            break
        
def close_client(client_socket):
    global is_running
    is_running = False
    client_socket.close()
    print("Cliente fechado com sucesso.")

def send_message(client_socket, server_address, message):
    client_socket.sendto(f"{user_nickname}: {message}".encode('utf-8'), server_address)

def send_private_message(client_socket, server_address, recipient, message):
    formatted_message = f"/MSG {recipient} {message}"
    client_socket.sendto(formatted_message.encode('utf-8'), server_address)

def send_file(client_socket, server_address, command):
    parts = command.split()
    if len(parts) >= 3:
        recipient = parts[1]
        file_path = parts[2]
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                file_size = len(file_data)
                header = f'/FILE {recipient} {os.path.basename(file_path)} {file_size}'.encode('utf-8')
                client_socket.sendto(header, server_address)
                client_socket.sendto(file_data, server_address)
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
    global is_running
    while True:
        message = input("-> ")
        if message.startswith("/"):
            if message.strip() == "/QUIT":
                print("Saindo do chat...")
                client_socket.sendto("/QUIT".encode('utf-8'), server_address)
                break
            process_command(client_socket, server_address, message)
        else:
            print('Comando desconhecido')
    close_client(client_socket)

def register_user(client_socket, server_address):
    global user_nickname
    nickname = input("Digite seu apelido para registro: ")
    if nickname:
        user_nickname = nickname
        client_socket.sendto(f"/REG {nickname}".encode('utf-8'), server_address)

def list_commands():
    print("Comandos disponíveis:")
    print("Digite uma mensagem e pressione enter para enviar para todos os usuários da sala.")
    print("/LIST - Lista todos os usuários conectados.")
    print("/MSG <usuario> <mensagem> - Envia uma mensagem privada para o usuário especificado.")
    print('/S <mensagem> - Envia uma mensagem para todos os usuários da sala.')
    print("/SEND <usuario> <caminho_do_arquivo> - Envia um arquivo para o usuário especificado.")
    print("/QUIT - Sai do chat.")


def main():
    server_host = '127.0.0.1'
    server_port = 5555
    server_address = (server_host, server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    register_user(client_socket, server_address)
    list_commands()
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    handle_user_input(client_socket, server_address)
    receive_thread.join()


if __name__ == "__main__":
    main()

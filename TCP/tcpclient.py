import socket
import threading

# Variável global para armazenar o nickname do usuário
user_nickname = None


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(2048)
            print(data.decode('utf-8'))
        except:
            print("Erro ao receber dados do servidor.")
            client_socket.close()
            break


def handle_user_input(client_socket):
    while True:
        message = input("-> ")
        if message.startswith("/"):
            if message.strip() == "/LIST":
                client_socket.send("/LIST".encode('utf-8'))
            else:
                process_command(client_socket, message)
        else:
            send_message(client_socket, message)


def send_message(client_socket, message):
    formatted_message = f"{user_nickname}: {message}"
    client_socket.send(formatted_message.encode('utf-8'))


def send_private_message(client_socket, recipient, message):
    formatted_message = f"/MSG {recipient} : {message}"
    client_socket.send(formatted_message.encode('utf-8'))


def process_command(client_socket, command):
    parts = command.split(maxsplit=2)
    if command.startswith("/QUIT"):
        print("Saindo do chat.")
        client_socket.close()
        exit()
    elif command.startswith("/MSG") and len(parts) > 2:
        send_private_message(client_socket, parts[1], parts[2])
    else:
        print("Comando desconhecido.")


def register_user(client_socket):
    global user_nickname
    while True:
        nickname = input("Digite seu apelido para registro: ")
        if nickname:
            user_nickname = nickname
            client_socket.send(f"/REG {nickname}".encode('utf-8'))
            break
        else:
            print("Por favor, insira um apelido válido.")


def list_commands():
    print("Comandos disponíveis:")
    print("Digite uma mensagem e pressione enter para enviar para todos os usuários da sala.")
    print("/MSG <nome> <mensagem>: Envia uma mensagem privada para um usuário específico.")
    print("/LIST: Lista todos os usuários conectados.")
    print("/QUIT: Sair do chat.")


SERVER = '127.0.0.1'
PORT = 5555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER, PORT))
register_user(client_socket)
list_commands()
receive_thread = threading.Thread(
    target=receive_messages, args=(client_socket,))
receive_thread.start()
send_message_thread = threading.Thread(
    target=handle_user_input, args=(client_socket,))
send_message_thread.start()

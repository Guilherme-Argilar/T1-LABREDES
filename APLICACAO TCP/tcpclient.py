import socket
import threading
import os

# Variável global para armazenar o nickname do usuário e o estado de execução
user_nickname = None
is_running = True

#funcao que trata as mensagens recebidas do servidor
def receive_messages(client_socket):
    global is_running
    try:
        while is_running:
            data = client_socket.recv(2048)
            if not data:
                break
            if data.startswith(b'/FILE'):
                handle_file_reception(data, client_socket)
            else:
                print(data.decode('utf-8'))
    except Exception as e:
        if is_running:
            print(f"Erro ao receber dados: {e}")
    finally:
        client_socket.close()
        print("Conexão encerrada pelo servidor.")

#funcao para fechar o cliente e encerrar a execucao corretamente
def close_client(client_socket):
    global is_running
    is_running = False
    try:
        client_socket.send("/QUIT".encode('utf-8'))
        client_socket.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        print(f"Erro ao enviar comando de desconexão: {e}")
    client_socket.close()
    print("Cliente fechado com sucesso.")

#funcao para tratar a entrada do usuario
def handle_user_input(client_socket):
    global is_running
    while True:
        message = input("-> ")
        if message.startswith("/"):
            if message.startswith("/QUIT"):
                print("Saindo do chat.")
                break
            elif message.strip() == "/LIST":
                client_socket.send("/LIST".encode('utf-8'))
            elif message.startswith("/SEND"):
                send_file(client_socket, message)
            elif message.startswith("/S"):
                send_message(client_socket, message)
            else:
                #caso não seja nenhum dos comandos acima, envia a mensagem para ser processada, ou seja
                #ou a mensagem é uma mensagem privada ou um comando desconhecido
                process_command(client_socket, message)
        else:
            print('comando desconhecido')
    close_client(client_socket)


def process_command(client_socket, command):
    parts = command.split(maxsplit=2)
    if command.startswith("/MSG") and len(parts) > 2:
        send_private_message(client_socket, parts[1], parts[2])
    else:
        print("Comando desconhecido.")

#funcao para enviar uma mensagem para todos os clientes conectados
def send_message(client_socket, message):
    formatted_message = f"{user_nickname}: {message}"
    client_socket.send(formatted_message.encode('utf-8'))

#funcao para enviar uma mensagem privada para um cliente especifico
def send_private_message(client_socket, recipient, message):
    #verifica se o comando foi construido corretamente, com destinatario e mensagem
    formatted_message = f"/MSG {recipient} {message}"
    client_socket.send(formatted_message.encode('utf-8'))

#funcao para enviar um arquivo para um cliente especifico
def send_file(client_socket, command):
    parts = command.split()
    #verifica se o comando possui destinatario e caminho do arquivo
    if len(parts) >= 3:
        recipient = parts[1]
        file_path = parts[2]
        try:
            #verifica se o arquivo existe e envia o arquivo para o destinatario
            with open(file_path, 'rb') as file:
                file_data = file.read()
                header = f'/SEND {recipient} {os.path.basename(file_path)}'.encode('utf-8')
                client_socket.send(header + b' ' + file_data)
        except FileNotFoundError:
            print("Arquivo não encontrado.")

#funcao para tratar a recepcao de um arquivo
def handle_file_reception(data, client_socket):
    _, filename, file_data = data.split(b' ', 2)
    with open(filename.decode('utf-8'), 'wb') as file:
        file.write(file_data)
    print(f"Arquivo {filename.decode('utf-8')} recebido.")

#funcao para registrar o usuario no servidor
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

#funcao para listar os comandos disponiveis ao cliente
def list_commands():
    print("Comandos disponíveis:")
    print("Digite uma mensagem e pressione enter para enviar para todos os usuários da sala.")
    print("/LIST - Lista todos os usuários conectados.")
    print("/MSG <usuario> <mensagem> - Envia uma mensagem privada para o usuário especificado.")
    print('/S <mensagem> - Envia uma mensagem para todos os usuários da sala.')
    print("/SEND <usuario> <caminho_do_arquivo> - Envia um arquivo para o usuário especificado.")
    print("/QUIT - Sai do chat.")

#funcao principal do cliente
def main():
    server_host = '127.0.0.1'
    server_port = 5555
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        print("Conectado ao servidor!")
        register_user(client_socket)
        list_commands()
        #inicia uma thread para receber mensagens do servidor
        threading.Thread(target=receive_messages, args=(client_socket,)).start()
        handle_user_input(client_socket)
    except Exception as e:
        print(f"Não foi possível conectar ao servidor: {e}")
        client_socket.close()

if __name__ == "__main__":
    main()

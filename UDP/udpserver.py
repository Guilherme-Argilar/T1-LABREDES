import socket

all_nicknames = {}

def handle_message(data, client_address, server_socket):
    print(f"Dado recebido de {client_address}: {data}")
    try:
        decoded_data = data.decode('utf-8')
        parts = decoded_data.split(' ', 3)
        command = parts[0]

        if command == "/REG":
            nickname = parts[1]
            all_nicknames[nickname] = client_address
            print(f"{nickname} registrado do endereço {client_address}.")

        elif command.startswith("/FILE"):
            sender, filename, file_size = parts[1], parts[2], int(parts[3])
            print(f"Esperando receber arquivo {filename} de tamanho {file_size} bytes de {sender}")
            file_data, _ = server_socket.recvfrom(file_size)
            with open(f"{filename}", 'wb') as file:
                file.write(file_data)
            print(f"Arquivo {filename} recebido de {sender}.")

        elif command.startswith("/MSG"):
            recipient, message = parts[1], parts[2]
            if recipient in all_nicknames:
                server_socket.sendto(message.encode('utf-8'), all_nicknames[recipient])

        elif command == "/LIST":
            list_message = ", ".join(all_nicknames.keys())
            server_socket.sendto(f"Usuários conectados: {list_message}".encode('utf-8'), client_address)

        else:
            broadcast_message(data, client_address, server_socket)
    except Exception as e:
        print(f"Erro ao processar dados: {e}")


def broadcast_message(message, sender_address, server_socket):
    for nickname, address in all_nicknames.items():
        if address != sender_address:
            server_socket.sendto(message, address)

def listen_for_messages(server_socket):
    while True:
        data, client_address = server_socket.recvfrom(2048)
        handle_message(data, client_address, server_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 5555))
    print("Servidor iniciado e ouvindo em UDP no porto 5555.")
    listen_for_messages(server_socket)

if __name__ == "__main__":
    start_server()

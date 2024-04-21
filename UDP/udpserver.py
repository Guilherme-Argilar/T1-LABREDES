import socket
import threading

def handle_message(data, client_address, all_nicknames, server_socket):
    message_parts = data.decode().split(' ', 2)
    command = message_parts[0]
    if command == "/REG":
        nickname = message_parts[1]
        all_nicknames[nickname] = client_address
        print(f"{nickname} registrado do endereço {client_address}.")
    elif command == "/MSG" and len(message_parts) > 2:
        recipient = message_parts[1]
        message = message_parts[2]
        if recipient in all_nicknames:
            recipient_address = all_nicknames[recipient]
            server_socket.sendto(f"Msg privada de {data.decode()}".encode('utf-8'), recipient_address)
    else:
        broadcast_message(data, client_address, all_nicknames, server_socket)

def broadcast_message(message, sender_address, all_nicknames, server_socket):
    for nickname, address in all_nicknames.items():
        if address != sender_address:
            server_socket.sendto(message, address)

def listen_for_messages(server_socket, all_nicknames):
    while True:
        data, client_address = server_socket.recvfrom(2048)
        handle_message(data, client_address, all_nicknames, server_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 5555))
    all_nicknames = {}
    print("Servidor iniciado e ouvindo em UDP no porto 5555.")
    listen_for_messages(server_socket, all_nicknames)

if __name__ == "__main__":
    start_server()

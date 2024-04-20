
import socket
import threading


def client_thread(conn, all_connections, all_nicknames):
    while True:
        try:
            data = conn.recv(2048)
            if data:
                if data.startswith(b'/SEND'):
                    handle_file_sending(data, all_nicknames)
                elif data.decode().startswith("/LIST"):
                    list_message = ", ".join(all_nicknames.keys())
                    conn.send(f"Users connected: {
                              list_message}".encode('utf-8'))
                elif data.decode().startswith("/REG"):
                    nickname = data.decode().split(' ')[1]
                    all_nicknames[nickname] = conn
                elif data.decode().startswith("/MSG"):
                    parts = data.decode().split(' ', 2)
                    if len(parts) > 2:
                        sender = [nick for nick,
                                  c in all_nicknames.items() if c == conn][0]
                        recipient = parts[1]
                        message = parts[2]
                        recipient_conn = all_nicknames.get(recipient)
                        if recipient_conn:
                            formatted_message = f"Msg privada de {
                                sender}: {message}"
                            recipient_conn.send(
                                formatted_message.encode('utf-8'))
                else:
                    broadcast_message(data, conn, all_connections)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            remove_client(conn, all_nicknames, all_connections)


def broadcast_message(message, sender_conn, all_connections):
    decoded_message = message.decode('utf-8')
    command_start_index = decoded_message.find("/S")
    message_content = decoded_message[:command_start_index] + \
        decoded_message[command_start_index + 3:]
    encoded_message = message_content.encode('utf-8')
    for client_conn in all_connections:
        if client_conn != sender_conn:
            client_conn.send(encoded_message)


def handle_file_sending(data, all_nicknames):
    _, recipient, filename = data.split(b' ', 2)
    recipient_conn = all_nicknames.get(recipient.decode('utf-8'))
    if recipient_conn:
        recipient_conn.send(b'/FILE ' + filename)


def remove_client(conn, all_nicknames, all_connections):
    nickname_to_remove = [nick for nick,
                          c in all_nicknames.items() if c == conn]
    if nickname_to_remove:
        del all_nicknames[nickname_to_remove[0]]
    all_connections.remove(conn)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen()
    all_connections = []
    all_nicknames = {}
    while True:
        client_conn, client_addr = server_socket.accept()
        all_connections.append(client_conn)
        threading.Thread(target=client_thread, args=(
            client_conn, all_connections, all_nicknames)).start()


if __name__ == "__main__":
    start_server()

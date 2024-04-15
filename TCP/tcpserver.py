import socket
import threading


def client_thread(conn, all_connections, all_nicknames):
    while True:
        try:
            data = conn.recv(2048)
            if data:
                decoded_data = data.decode()
                if decoded_data.startswith("/LIST"):
                    # Enviar lista de usuários conectados
                    list_message = ", ".join(all_nicknames.keys())
                    conn.send(
                        f"Users connected: {list_message}".encode('utf-8'))
                elif decoded_data.startswith("/REG"):
                    nickname = decoded_data.split(' ')[1]
                    # Associar conexão ao nickname
                    all_nicknames[nickname] = conn
                elif decoded_data.startswith("/MSG"):
                    parts = decoded_data.split(' ', 2)
                    if len(parts) > 2:
                        sender = [nick for nick,
                                  c in all_nicknames.items() if c == conn][0]
                        recipient = parts[1]
                        message = parts[2]
                        recipient_conn = all_nicknames.get(recipient)
                        if recipient_conn:
                            # Formatar mensagem para exibir como mensagem privada do remetente
                            formatted_message = f"Msg privada de {sender}: {message}"
                            recipient_conn.send(
                                formatted_message.encode('utf-8'))
                else:
                    # Corrigir o loop para não reutilizar a variável 'conn'
                    for client_conn in all_connections:
                        if client_conn != conn:
                            client_conn.send(data)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            # Remover conexão e nickname adequadamente
            nickname_to_remove = [nick for nick,
                                  c in all_nicknames.items() if c == conn]
            if nickname_to_remove:
                del all_nicknames[nickname_to_remove[0]]
            all_connections.remove(conn)
            break


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen()
    all_connections = []
    all_nicknames = {}  # Usar um dicionário para armazenar nicknames e suas conexões
    while True:
        client_conn, client_addr = server_socket.accept()
        all_connections.append(client_conn)
        threading.Thread(target=client_thread, args=(
            client_conn, all_connections, all_nicknames)).start()


if __name__ == "__main__":
    start_server()

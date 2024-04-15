import socket
import threading


def client_thread(conn, all_connections, all_addresses):
    while True:
        try:
            data = conn.recv(2048)
            if data:
                header = data.split(b' ', 3)
                if header[0] == b"/FILE" and len(header) > 3:
                    recipient = header[1].decode('utf-8')
                    filename = header[2].decode('utf-8')
                    file_data = header[3]
                    recipient_conn = next(
                        (c for c, a in zip(all_connections, all_addresses) if a[0] == recipient), None)
                    if recipient_conn:
                        recipient_conn.send(
                            f"Received file {filename}".encode('utf-8') + file_data)
                else:
                    for client in all_connections:
                        if client != conn:
                            client.send(data)
        except:
            conn.close()
            all_connections.remove(conn)
            break


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen()
    all_connections = []
    all_addresses = []
    while True:
        client_conn, client_addr = server_socket.accept()
        all_connections.append(client_conn)
        all_addresses.append(client_addr)
        threading.Thread(target=client_thread, args=(
            client_conn, all_connections, all_addresses)).start()


if __name__ == "__main__":
    start_server()

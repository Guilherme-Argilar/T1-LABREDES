import socket
import threading

def client_thread(conn, all_connections, all_nicknames):
#funcao para tratar as mensagens recebidas de um cliente de acordo com o comando especificado no inicio da mensagem
    while True:
        try:
            data = conn.recv(2048)
            client_address = conn.getpeername()
            if not data:
                raise Exception("Cliente desconectado")
            print(f"Dado recebido de {client_address}: {data}")
            
            if data.startswith(b'/SEND'):
                handle_file_sending(data, all_nicknames)
            elif data.decode().startswith("/LIST"):
                list_message = ", ".join(all_nicknames.keys())
                conn.send(f"Usuarios conectados: {list_message}".encode('utf-8'))
            elif data.decode().startswith("/REG"):
                nickname = data.decode().split(' ')[1]
                all_nicknames[nickname] = conn
            elif data.decode().startswith("/QUIT"):
                raise Exception("Client solicitou finalizacao da conexao")
            elif data.decode().startswith("/MSG"):
                parts = data.decode().split(' ', 2)
                #verifica se a mensagem possui destinatario e conteudo
                if len(parts) > 2:
                    #verifica se o destinatario esta conectado
                    sender = [nick for nick, c in all_nicknames.items() if c == conn][0]
                    recipient, message = parts[1], parts[2]
                    recipient_conn = all_nicknames.get(recipient)
                    #envia a mensagem privada para o destinatario
                    if recipient_conn:
                        formatted_message = f"Mensagem privada de {sender}: {message}"
                        recipient_conn.send(formatted_message.encode('utf-8'))
            else:
                broadcast_message(data, conn, all_connections)
        except Exception as e:
            print(f"Error from {client_address}: {e}")
            break
    remove_client(conn, all_nicknames, all_connections)

#funcao para enviar uma mensagem para todos os clientes conectados, exceto o remetente
def broadcast_message(message, sender_conn, all_connections):
    decoded_message = message.decode('utf-8')
    command_start_index = decoded_message.find("/S ")
    if command_start_index != -1:
        message_content = decoded_message[command_start_index + 3:]
        encoded_message = message_content.encode('utf-8')
        for client_conn in all_connections:
            if client_conn != sender_conn:
                client_conn.send(encoded_message)

#funcao para enviar um arquivo para um cliente especifico passado pelo data
def handle_file_sending(data, all_nicknames):
    _, recipient, filename = data.split(b' ', 2)
    recipient_conn = all_nicknames.get(recipient.decode('utf-8'))
    if recipient_conn:
        recipient_conn.send(b'/FILE ' + filename)

#funcao para remover um cliente da lista de conexoes e nicknames
def remove_client(conn, all_nicknames, all_connections):
    nickname_to_remove = [nick for nick, c in all_nicknames.items() if c == conn]
    if nickname_to_remove:
        del all_nicknames[nickname_to_remove[0]]
    all_connections.remove(conn)
    conn.close()
    print(f"Conexao finalizada e usuario {nickname_to_remove[0] if nickname_to_remove else 'desconhecido'} removido.")


#funcao principal para iniciar o servidor, configura a porta e inicia a escuta
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen()
    all_connections = []
    all_nicknames = {}
    print(" Servidor Iniciado e ouvingo na porta 5555")
    #loop para aceitar novas conexoes e criar uma thread para tratar cada uma
    while True:
        client_conn, client_addr = server_socket.accept()
        all_connections.append(client_conn)
        print(f"Nova conexao: {client_addr}")
        threading.Thread(target=client_thread, args=(client_conn, all_connections, all_nicknames)).start()

if __name__ == "__main__":
    start_server()

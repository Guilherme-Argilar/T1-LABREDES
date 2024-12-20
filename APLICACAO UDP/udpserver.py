import socket
#dicionario para armazenar os nicknames dos clientes conectados
all_nicknames = {}

#funcao para tratar as mensagens recebidas de um cliente de acordo com o comando especificado no inicio da mensagem
def handle_message(data, client_address, server_socket):
    print(f"Dado recebido de {client_address}: {data}")
    try:
        #decodifica a mensagem recebida
        decoded_data = data.decode('utf-8')
        parts = decoded_data.split(' ', 3)
        command = parts[0]
        #Adicina um nickname ao dicionario de nicknames
        if command == "/REG":
            nickname = parts[1]
            all_nicknames[nickname] = client_address
            print(f"{nickname} registrado do endereço {client_address}.")

        elif command.startswith("/FILE"):
            try:
                #verifica se o comando foi construido corretamente, com destinatario, nome do arquivo e tamanho do arquivo
                recipient, filename, file_size = parts[1], parts[2], int(parts[3])
                print(f"Esperando receber arquivo {filename} de tamanho {file_size} bytes")
                file_data, _ = server_socket.recvfrom(file_size)
                if recipient in all_nicknames:
                    #envia o arquivo para o destinatario
                    header = f"/FILE {filename} {file_size}".encode('utf-8')
                    server_socket.sendto(header, all_nicknames[recipient])
                    server_socket.sendto(file_data, all_nicknames[recipient])
                    print(f"Arquivo {filename} enviado para {recipient}.")
            except Exception as e:
                print(f"Erro ao processar dados: {e}")

        elif command == "/QUIT":
            nickname = [nick for nick, addr in all_nicknames.items() if addr == client_address]
            if nickname:
                del all_nicknames[nickname[0]]
                print(f"{nickname[0]} saiu do chat.")
        
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

#funcao para enviar uma mensagem para todos os clientes conectados
def broadcast_message(message, sender_address, server_socket):
    for nickname, address in all_nicknames.items():
        #envia a mensagem para todos os clientes conectados, exceto o remetente
        if address != sender_address:
            server_socket.sendto(message, address)

#funcao para ouvir mensagens
def listen_for_messages(server_socket):
    while True:
        #fica escutando até receber uma mensagem de algum client
        data, client_address = server_socket.recvfrom(2048)
        handle_message(data, client_address, server_socket)



#funcao para iniciar o servidor
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 5555))
    print("Servidor iniciado e ouvindo em UDP no porto 5555.")
    listen_for_messages(server_socket)

if __name__ == "__main__":
    start_server()

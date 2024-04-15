# Chat System using Sockets

Este projeto implementa um sistema básico de chat utilizando sockets TCP e UDP em Python. Ele permite a comunicação entre um servidor e múltiplos clientes em uma rede local. Os usuários podem enviar mensagens públicas no chat, enviar mensagens privadas para usuários específicos e visualizar a lista de usuários conectados.

## Funcionalidades

- **Conexão de múltiplos clientes**: Vários clientes podem se conectar ao servidor e trocar mensagens.
- **Envio de mensagens públicas**: Usuários podem enviar mensagens que serão vistas por todos os usuários conectados.
- **Mensagens privadas**: Usuários podem enviar mensagens privadas para um usuário específico.
- **Listagem de usuários**: Usuários podem solicitar a lista de todos os usuários conectados no momento.
- **Registro de usuário**: Novos usuários podem registrar um apelido ao se conectar.

## Requisitos

Para executar este projeto, você precisará de Python 3.6 ou superior.

## Como executar

1. Clone o repositório:
    ```bash
    git clone https://github.com/Guilherme-Argilar/T1-LABREDES
    ```

2. Inicie o servidor:
    ```bash
    python server.py
    ```

3. Em outra(s) janela(s) de terminal, inicie o(s) cliente(s):
    ```bash
    python client.py
    ```

4. Siga as instruções na tela para registrar um apelido e começar a enviar mensagens.

## Comandos disponíveis

- **Mensagem pública**: Apenas digite sua mensagem e pressione enter.
- **Mensagem privada**: `/MSG <nome> <mensagem>`
- **Listar usuários**: `/LIST`
- **Sair do chat**: `/QUIT`

## Estrutura do código

- `client.py`: Contém a lógica do cliente para conectar-se ao servidor, enviar e receber mensagens.
- `server.py`: Gerencia todas as conexões dos clientes, processa as mensagens e comandos recebidos.

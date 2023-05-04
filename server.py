import socket
import threading
from datetime import datetime

HOST = ''
PORT = 5000
BUFFER_SIZE = 1024

# Lista de clientes conectados
clients = []

# Nome da sala
room_name = "Sala de Bate-papo"

# Inicia o servidor
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor iniciado na sala '{room_name}', aguardando conexões...")

    # Aguarda conexões de novos clientes
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nova conexão de {addr[0]}:{addr[1]}")

        # Envia o nome da sala para o novo cliente
        client_socket.send(f"Bem-vindo à sala '{room_name}'!\n\n".encode())

        # Adiciona o cliente à lista de clientes conectados
        clients.append(client_socket)

        # Inicia uma thread para tratar as mensagens recebidas do cliente
        thread = threading.Thread(target=handle_client_messages, args=(client_socket,))
        thread.start()

# Trata as mensagens recebidas do cliente
def handle_client_messages(client_socket):
    # Recebe o nome de usuário do cliente
    username = client_socket.recv(BUFFER_SIZE).decode().strip()

    # Envia mensagem de boas-vindas ao novo usuário
    client_socket.send(f"Olá, {username}! Bem-vindo à sala '{room_name}'!\n\n".encode())

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode()

            # Verifica se a mensagem não está vazia
            if message:
                # Formata a mensagem com o nome do autor e a hora e data de envio
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
                formatted_message = f"[{timestamp}] {username}: {message}"
                print(formatted_message)

                # Envia a mensagem para todos os clientes conectados, exceto o próprio autor
                for client in clients:
                    if client != client_socket:
                        client.send(formatted_message.encode())

        except:
            # Remove o cliente da lista de clientes conectados e encerra a thread
            clients.remove(client_socket)
            client_socket.close()
            print(f"{username} desconectado. {len(clients)} clientes conectados.")
            break

# Inicia o servidor
start_server()

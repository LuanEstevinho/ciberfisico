import socket as sock
import threading


lista_clientes = []


def broadcast(mensagem, remetente=None):
    for cliente in lista_clientes:
        if cliente["socket"] != remetente: 
            try:
                cliente["socket"].sendall(mensagem.encode())
            except:
                lista_clientes.remove(cliente)

def unicast(mensagem, destinatario_nome):
    for cliente in lista_clientes:
        if cliente["nome"] == destinatario_nome:
            try:
                cliente["socket"].sendall(mensagem.encode())
                return True
            except:
                lista_clientes.remove(cliente)
                return False
    return False  

def recebe_mensagem(sock_conn, ender):
 
    nome = sock_conn.recv(50).decode()
    print(f"Conexão com {nome} - {ender}")
    
 
    lista_clientes.append({"nome": nome, "socket": sock_conn})
    broadcast(f"{nome} entrou no chat!", remetente=sock_conn)
    
    while True:
        try:
            mensagem = sock_conn.recv(1024).decode()
            print(f"{nome} enviou: {mensagem}")

            if mensagem.startswith("@"):
                partes = mensagem.split(" ", 1)
                if len(partes) > 1:
                    destinatario_nome = partes[0][1:]  
                    mensagem_unicast = partes[1]       
                    enviado = unicast(f"[Privado de {nome}]: {mensagem_unicast}", destinatario_nome)
                    if not enviado:
                        sock_conn.sendall(f"Usuário {destinatario_nome} não encontrado.".encode())
                else:
                    sock_conn.sendall("Comando inválido. Use: @nome_destinatario mensagem".encode())
            else:
                broadcast(f"{nome}: {mensagem}", remetente=sock_conn)

        except:
            lista_clientes.remove({"nome": nome, "socket": sock_conn})
            broadcast(f"{nome} saiu do chat")
            sock_conn.close()
            break


HOST = '172.20.10.10'  # IP do servidor
PORTA = 7777         # Porta do servidor1

sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
sock_server.bind((HOST, PORTA))
sock_server.listen()

print(f"O servidor {HOST}:{PORTA} espera por conexões.")


while True:
    conn, ender = sock_server.accept()
    threadCliente = threading.Thread(target=recebe_mensagem, args=[conn, ender])
    threadCliente.start()

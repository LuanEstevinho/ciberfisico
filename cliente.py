import socket as sock
import threading

HOST = '172.20.10.10'  # IP do servidor
PORTA = 7777            # Porta do servidor


socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)


socket_cliente.connect((HOST, PORTA))
print(10 * "*" + " O Chat foi Iniciado! " + 10 * "*")


nome = input("Digite aqui seu nome: ")
socket_cliente.sendall(nome.encode())
print("Digite '/sair' para sair do chat!")
print("Para enviar mensagem privada, use o formato: @nome_destinatario mensagem")

def receber_mensagens():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            if mensagem:
                print(f"\n{mensagem}")
        except:
            print("Erro ao receber mensagem do servidor...")
            socket_cliente.close()
            break


thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()


while True:
    try:
        mensagem = input('\nDigite sua mensagem: ')
        if mensagem.lower() == "/sair":
            print("Você saiu do chat")
            socket_cliente.close()
            break
        socket_cliente.sendall(mensagem.encode())
    except:
        print("Ocorreu um erro no envio da mensagem!")
        socket_cliente.close()
        break

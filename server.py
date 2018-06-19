import socket
import _thread
from random import randint

clientes = []

def post_message(socket,message):
    for cliente in clientes:
        print("Enviando "+ message + " para ")
        print(cliente)
        socket.sendto(message.encode(),cliente)

def Cliente_Thread(cliente):
    new_bind = False
    new_host = '10.40.131.9'
    new_port = randint(10000, 64000)
    message = ""
    user_name = ""
    user_message = ""

    #Abre um novo socket para tratar o cliente.
    thread_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while(new_bind == False):
        try:
            #print("Tentando o bind na porta %d\n" % new_port)
            new_addr = (new_host,new_port)
            thread_sock.bind(new_addr)
            new_bind = True
        except:
            new_port = randint(10000, 64000)
            #print ("criando nova porta %d \n" % new_port)

    #print("Novo socket aberto\n")
    
    # Envia a nova porta para o cliente
    message = "NEW_PORT".encode()
    thread_sock.sendto(message,cliente)
    #Espera ACK
    #print("Esperando ACK da nova porta\n")
    msg, cliente = thread_sock.recvfrom(1024)
    
    #Pergunta o nome do usuário
    #print ("ACK Recebido, enviando get_id\n")
    message = "Nome de usuário: ".encode()
    thread_sock.sendto(message,cliente)

    #Espera a resposta
    msg, cliente = thread_sock.recvfrom(1024)
    user_name = msg.decode()

    #Trata mensagens do cliente
    #print ("Conexão estabelecida com o cliente.\n")
    user_message = user_name + " entrou."
    post_message(thread_sock,user_message)
    while (True):
        msg, cliente = thread_sock.recvfrom(1024)
        user_message = user_name + ": " + msg.decode()
        post_message(thread_sock,user_message)




#INICIO DO PROGRAMA
HOST = '10.40.131.9'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
clientes = []

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)

while True:
    msg, cliente = udp.recvfrom(1024)
    if (msg.decode() == "HELLO"):
        print("New Client.\n")
        clientes.append(cliente)
        _thread.start_new_thread(Cliente_Thread,(cliente,))
    else:
        pass


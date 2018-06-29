import socket
import _thread
from random import randint

clientes = []
HOST = input("Enter host address: ")
PORT = 5000

def post_message(socket,message):   #Função para enviar uma mensagem para todos
    for cliente in clientes:        #os clientes. 
        print("Enviando "+ message + " para ")
        print(cliente)
        socket.sendto(message.encode(),cliente)

def Cliente_Thread(cliente):    #Thread para atender cada cliente, é criada uma para
    new_bind = False            #cada cliente
    new_host = HOST
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
PORT = 5000            # Porta que o Servidor esta
clientes = []

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)      #Cria Socket no host e porta especificado para receber
                    #conexões de clientes.

while True:
    #Servidor fica em loop infinito esperando novas conexões, cada
    #vez que o servidor recebe HELLO de um cliente, ele cria uma thread
    #para atendê-lo exclusivamente e insere esse cliente na lista de clientes.
    msg, cliente = udp.recvfrom(1024)    
    if (msg.decode() == "HELLO"):
        print("New Client.\n")
        clientes.append(cliente)
        _thread.start_new_thread(Cliente_Thread,(cliente,))
    else:
        pass


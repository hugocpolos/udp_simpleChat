#####################################
# 
# Chat UDP - Aplicação servidor
# Autor: Hugo Constantinopolos.
# Disponível em : https://github.com/hugocpolos/udp_simpleChat
#
#####################################

#####################################
# ÁREA DE IMPORT
import socket
import _thread
from random import randint
#####################################

#####################################
# Função para enviar uma mensagem para
# todos os outros clientes.
#
def post_message(socket,message):   #Função para enviar uma mensagem para todos
    for cliente in clientes:        #os clientes. 
        print("Enviando "+ message + " para ")
        print(cliente)
        socket.sendto(message.encode(),cliente)
#
#####################################

#####################################
# Thread para tratamento de um cliente
# O servidor roda uma para cada
# cliente conectado.
#
#
def Cliente_Thread(cliente):
    # Inicialização das variáveis locais.
    new_bind = False
    new_host = HOST
    new_port = randint(10000, 64000)
    message = ""
    user_name = ""
    user_message = ""

    #Abre um novo socket para tratar o cliente.
    thread_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Laço para realizar o bind na nova porta gerada aleatoriamente,
    # enquanto a porta estiver ocupada, será gerada uma nova porta
    # e realizado nova tentativa de bind.
    while(new_bind == False):
        try:
            #print("Tentando o bind na porta %d\n" % new_port)
            new_addr = (new_host,new_port)
            thread_sock.bind(new_addr)
            new_bind = True
        except:
            new_port = randint(10000, 64000)
            #print ("criando nova porta %d \n" % new_port)

    
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

    #Espera a resposta com o nome de usuário.
    msg, cliente = thread_sock.recvfrom(1024)
    user_name = msg.decode()

    # Nesse momento o cliente está conectado.
    # é enviado a mensagem "Usuário entrou."
    # para os clientes.
    user_message = user_name + " entrou."
    post_message(thread_sock,user_message)

    ######################################
    # Laço para receber mensagens do cliente, tratá-las
    # e enviá-las para os demais clientes.
    while (True):
        msg, cliente = thread_sock.recvfrom(1024)
        user_message = user_name + ": " + msg.decode()
        post_message(thread_sock,user_message)
    #
    ######################################
#
###################################


###################################
# INICIO DO PROGRAMA 
#
###################################
# Inicialização da lista de clientes conectados
# e do socket para a conexão de novos clientes.
#
clientes = []
HOST = input("Enter host address: ")
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)      #Cria Socket no host e porta especificado para receber
                    #conexões de clientes.
###################################

###################################
# 
# Laço para receber novos clientes,
# sempre que um novo cliente é conectado,
# é criado uma thread para tratá-lo
# e o cliente é inserido na lista de
# clientes conectados.
#
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
#
##################################
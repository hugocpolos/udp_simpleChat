#####################################
# 
# Chat UDP - Aplicação cliente
# Autor: Hugo Constantinopolos.
# Disponível em : https://github.com/hugocpolos/udp_simpleChat
#
#####################################

#####################################
# ÁREA DE IMPORT
import socket
import _thread
from tkinter import *
#####################################

#####################################
# Inicialização da interface gráfica
window = Tk()
window.title("UDP Chat")
messages = Text(window)
messages.pack()
input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)
#####################################

#####################################
# Função chamada ao pressionar a tecla
# Enter. Envio de mensagens ao servidor
#
def Enter_pressed(event):
    input_get = input_field.get()

    message = input_get.encode()
    udp2.sendto(message, dest2)
    input_user.set('')
    return "break"
#
######################################

######################################
#
# Thread que recebe constantemente mensagens do servidor,
# ao receber uma mensagem ( message ), ele adiciona à
# interface gráfica (messages) e posiciona a tela na
# ultima mensagem recebida.
#
def listen(socket):
    while True:
        message, addr = udp.recvfrom(1024)
        messages.insert(INSERT, '%s\n' % message.decode())
        messages.see("end")
#
#######################################

######################################
#
# Inicialização da conexão UDP 
# com o servidor.
#
HOST = input("Enter server address: ")  # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
message = ""
#
######################################

######################################
# Conexão, obtenção da nova porta e
# envio do nome de usuário para o servidor
#
# Envia HELLO para o servidor
message = "HELLO".encode()
udp.sendto(message, dest)
#
# Espera nova porta
msg, server_addr = udp.recvfrom(1024)
new_port = int(server_addr[1])
print(new_port)
#
# Abre um novo socket para comunicação na nova porta.
udp2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest2 = (HOST, new_port)
# Envia ACK pela nova porta
# print("Enviando ACK")
message = "ACK".encode()
udp2.sendto(message, dest2)
#
# Espera requisição de nome de usuário
msg, server_addr = udp2.recvfrom(1024)
#
# Envia o nome de usuário 
message = input (msg.decode())
message = message.encode()
udp2.sendto(message, dest2)
#
#
print("Conexão realizada com sucesso.\n")
########################################

########################################
# Inicia a thread para receber mensagens.
_thread.start_new_thread(listen,(udp2,))
#
########################################

########################################
#
# Inicia a interface Gráfica
frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()
window.mainloop()
#
# Nesse ponto o programa está em um loop:
# Com a interface gráfica carregada, aguardando
# o usuário entrar uma mensagem e pressionar
# enter e aguardando e exibindo mensagens
# vindas do servidor ( de outros clientes.)
#######################################
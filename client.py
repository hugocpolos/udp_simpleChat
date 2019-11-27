#!/usr/bin/python3.7
"""
Chat UDP - Client Application
Author: Hugo Constantinopolos
        hugo.cpolos@gmail.com
Available at: https://github.com/hugocpolos/udp_simpleChat
"""

import socket
import _thread
import tkinter
from sys import argv


class Chat_GUI:

    """Class describing graphic user interface of the chat client.
    The GUI is built with the tkinter module.
    """

    def __init__(self, communication_socket, server_address):
        """This constructor method creates the user interface,
        creates its layout and its positioning.
        tkinter gui can be built according to the documentation
        available at https://tkdocs.com/

        Args:
            communication_socket (socket): socket that the gui has to send a
            server_address ((str,int)): tuple with the server adress, to send
            message after <Return> is pressed.
            a message when <Return> is pressed.

        Todo:
                make the gui not dependant of sockets and address.
        """
        self.__socket = communication_socket
        self.__server_address = server_address
        self.__window = tkinter.Tk()
        self.__window.title("UDP Chat")
        self.__messages = tkinter.Text(self.__window)
        self.__messages.pack()
        self.__input_user = tkinter.StringVar()
        self.__input_field = tkinter.Entry(self.__window, text=self.__input_user)
        self.__input_field.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.__frame = tkinter.Frame(self.__window)
        self.__frame.pack()
        self.__input_field.bind("<Return>", self.__enter_pressed)

    def start(self):
        """This method loads and starts the gui.
        """
        # The tkinter.Tk.mainloop method loads and starts the tkinter gui.
        self.__window.mainloop()

    def __enter_pressed(self, _):
        """Method to be executed when the "<Return>" key is pressed.

        Args:
            _ (KeyPress event): not used.
                This arg is received because its called by the tkinter method .bind()
                which always sends the KeyPress event as parameter.
        """
        message = self.__input_field.get().encode()
        self.__socket.sendto(message, self.__server_address)
        self.__input_user.set('')

    def insert_received_message_at_the_board(self, message):
        """Inserts a message at the message board.

        Args:
            message (str): string to be inserted at the board.
        """
        self.__messages.insert(tkinter.INSERT, '%s\n' % message.decode())
        self.__messages.see("end")


class Chat_Client:

    """Class that implements the login client of the udp chat application.
    It implements the login protocol, the socket and threading allocation,
    and the logic to get it working.

    Attributes:
        is_logged (bool): Describes if the client is logged or not.
    """

    def __init__(self):
        """Starts all needed public and private attributes as None or False.
        """
        self.__chat_server_login_address = None
        self.__chat_server_communication_address = None
        self.__chat_gui = None
        self.__sending_socket = None
        self.__login_and_listening_socket = None
        self.is_logged = False

    def connect_to_server(self, host, port):
        """This method implements the connection to a chat
        server available at (host,port).

        Args:
            host (str): hostname or ip of the server
            port (int): port to connect to the server
        """
        self.__set_server_address(host, port)
        self.__start_login_and_listening_socket()
        self.__login_to_server()
        if self.is_logged:
            self.__start_sending_socket()
            self.__chat_gui = Chat_GUI(self.__sending_socket, self.__chat_server_communication_address)
            self.__listen_to_server_messages()
            self.__chat_gui.start()

    def __set_server_address(self, host, port):
        """sets the tuple __chat_server_login_address,
        to be used as server address

        Args:
            host (str): hostname or ip of the server
            port (int): port to connect to the server
        """
        self.__chat_server_login_address = (host, port)

    def __start_login_and_listening_socket(self):
        """starts the socket that will be used to login to the server and
        then wait for other client's messages.
        """
        self.__login_and_listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __start_sending_socket(self):
        """starts the socket to be used to send message to the server.
        """
        self.__sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __send_message_to_server(self, message, login=False):
        """send a message to the udp chat server located at the attribute
        __chat_server_login_address, in case of the first login message. And
        __chat_server_communication_address, in case of other communications.

        Args:
            message (str): message to be sent.
            login (bool, optional): if true, the message will be sent to the login address. Otherwise,
                the message will be sent to the communication address opened just for this client.
        """
        if login:
            self.__login_and_listening_socket.sendto(message.encode(), self.__chat_server_login_address)
        else:  # if not login
            self.__login_and_listening_socket.sendto(message.encode(), self.__chat_server_communication_address)

    def __login_to_server(self):
        """Login protocol
        """
        # Sends HELLO to the server.
        self.__send_message_to_server("HELLO", login=True)

        # Waits for the new port, that the server opened to attend just this client.
        new_port = int(self.__login_and_listening_socket.recvfrom(1024)[1][1])

        # Store the tuple (server host, new_port) in the attribute __chat_server_communication_address.
        self.__chat_server_communication_address = (self.__chat_server_login_address[0], new_port)

        # Sends "ACK" to the new communication channel.
        self.__send_message_to_server("ACK")

        # Waits for the server to ask the client username.
        message = self.__login_and_listening_socket.recvfrom(1024)[0]

        # Display the message and waits for the user to enter its username.
        username = input(message.decode())

        # Send the username to the server.
        self.__send_message_to_server(username)

        # The client is now connected to the udp chat server.
        self.is_logged = True

    def __listen_to_server_messages(self):
        """method that calls the __listen_to_server_messages_thread method
        as a new thread.
        """
        _thread.start_new_thread(self.__listen_to_server_messages_thread, ())

    def __listen_to_server_messages_thread(self):
        """method that wait for messages comming from the server and put the
        messages on the GUI.
        """
        while True:
            message = self.__login_and_listening_socket.recvfrom(1024)[0]
            print(message.decode())
            self.__chat_gui.insert_received_message_at_the_board(message)


def main():
    """Main function of the program
    """
    if len(argv) is not 2:
        print(
            """
            Usage:
                %s <server_host_name>
            """ % (argv[0]))
        exit()

    c = Chat_Client()
    c.connect_to_server(argv[1], 5000)


if __name__ == '__main__':
    main()

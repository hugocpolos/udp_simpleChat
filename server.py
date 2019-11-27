#!/usr/bin/python3.7
"""
Chat UDP - Server Application
Author: Hugo Constantinopolos
        hugo.cpolos@gmail.com
Available at: https://github.com/hugocpolos/udp_simpleChat
"""

import socket
import _thread
import random


class Connected_Client:

    """Class describing a client connected to the
    chat server.

    Attributes:
        address ((str,int)): tuple containing the client address.
        username (str): client username
    """

    def __init__(self, host, port):
        """Constructor method for the Connected_Client class.
        It initializes a client at the given host and port.

        Args:
            host (str): hostname or ip of the client.
            port (int): udp port used to communicate with this client.
        """
        self.__host__ = host
        self.__port__ = port
        self.username = None
        self.address = (self.__host__, self.__port__)

    def __str__(self):
        """This method describes how the client is represented as a string.

        Returns:
            str: string in the format 'username@host:port'
        """
        return "%s@%s:%d" % (self.username, self.__host__, self.__port__)


class Chat_Server:

    """Class describing an UDP chat server.

    usage:
            s = Chat_Server(host,port)
            s.start()

        It creates an udp chat server listening at the given port.

    Attributes:
        host (str): host address of the server
        port (int): port where the server will wait for new connections
    """

    def __init__(self, port):
        """Constructor method of the class

        Args:
            port (int): port of the server
        """
        self.port = port
        self.host = None
        self.__connected_client = []
        self.__sending_socket = None
        self.__listen_socket = None
        self.__initialize_hostname()

    def start(self):
        """Starts the server.
        It initializes the socket that will listen for new connections
        and then call the function that wait for new connections.
        """
        self.__start_listen_socket()
        self.__wait_for_new_connections()

    def __initialize_hostname(self):
        """It sets the attribute 'host' to the name of the host running
        this script.
        """
        self.host = socket.gethostname()

    def __start_listen_socket(self):
        """It starts the listening socket.
        this socket is binded to the port given in the attribute 'port'
        """
        self.__listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__listen_socket.bind((self.host, self.port))

    def __start_sending_socket(self, port):
        """The method starts and returns a new socket binded at the port given by
        the 'port' argument

        Args:
            port (int): port which the socket will be binded.

        Returns:
            socket: An object containing the new socket.
        """
        __sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        __sending_socket.bind((self.host, port))
        return __sending_socket

    def __start_client_server_communication(self, client):
        """This method starts a new thread where the server will communicate
        with the client exclusively.

        Args:
            client (Connected_Client): client that the server will establish connection.
        """
        _thread.start_new_thread(self.__client_thread__, (client,))

    def __send_message_to_all_connected_clients(self, sending_socket, message):
        """Send a message to all connected clients.

        Args:
            sending_socket (socket): socket that will be used to send the message.
            message (string): string containing the message to be sent.
        """
        for client in self.__connected_client:
            print("Sending '%s' to %s." % (message, client))
            sending_socket.sendto(message.encode(), client.address)

    def __wait_for_new_connections(self):
        """This method will make the server start to listen at
        the port 'self.port' for new clients.
        """
        while True:
            msg, (client_host, client_port) = self.__listen_socket.recvfrom(1024)
            if (msg.decode() == "HELLO"):
                # print("New Client.")
                c = Connected_Client(client_host, client_port)
                self.__start_client_server_communication(c)
                self.__connected_client.append(c)
            else:
                pass

    def __login(self, sending_socket, client):
        """Method that implement the login protocol.

        Args:
            sending_socket (socket): socket that will be used to communicate.
            client (Connected_Client): client that will login to the chat server.
        """
        # Send a NEW_PORT message to the client.
        message = "NEW_PORT".encode()
        sending_socket.sendto(message, client.address)

        # Wait for the ACK message.
        message = sending_socket.recvfrom(1024)[0]

        # print ("ACK %s Recebido, enviando get_id" % (message.decode()))
        # send the 'please enter your username' message.
        message = "Please enter your username: ".encode()
        sending_socket.sendto(message, client.address)

        # Waits for the client username.
        message = sending_socket.recvfrom(1024)[0]
        client.username = message.decode()

        # Now, the client is connected.
        # the message 'username has joined the chat.' will be sent to all other users.
        message = client.username + " has joined the chat."
        self.__send_message_to_all_connected_clients(sending_socket, message)

    def __client_thread__(self, client):
        """method that will login the new username and listen for its messages.

        Args:
            client (Connected_Client): connected client.
        """
        new_port = random.randint(10000, 64000)
        print(new_port)
        sending_socket = self.__start_sending_socket(new_port)
        self.__login(sending_socket, client)

        # In this loop, the server will be continuosly waiting for the client messages
        # and then sending these messages to all connected clients.
        while (True):
            msg = sending_socket.recvfrom(1024)[0]
            message = client.username + ": " + msg.decode()
            self.__send_message_to_all_connected_clients(sending_socket, message)


def main():
    """Main function of the program
    """
    s = Chat_Server(5000)
    s.start()


if __name__ == '__main__':
    main()

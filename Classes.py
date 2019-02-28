import socket
import os
import sys
from GitRepo.RSA import generate_prime_file, generate_keys, encrypt, decrypt


def check_files_path(path):
    if os.path.exists(path):
        print("A file already exists in this path. Would you like to overwrite it ?")
        will = input("Enter y for yes or n for no:\t")
        while will != 'y' and will != 'n':
            will = input("Please enter y for yes or n for no. Do not enter any other character:\t")
        if will == 'n':
            sys.exit()
        else:
            return 'continue'
    return 'continue'


class Server:
    def __init__(self, addr, port, listens):
        self.port = port
        self.addr = addr
        self.listens = listens

    def socket_operations(self):
        server_socket = socket.socket()
        server_socket.bind((self.addr, self.port))
        server_socket.listen(self.listens)
        client_socket, client_address = server_socket.accept()
        return server_socket, client_socket

    def create_keys(self):
        """
        This method creates the public and private key using the generate_keys function.
        The public key will be sent to the client and the private key will be returned.
        """

        path = input("Enter a path your are reading from the prime numbers:\t")
        generate_prime_file(800, path)
        pub_key, priv_key = generate_keys(path)
        server_socket, client_socket = self.socket_operations()
        client_socket.send(str(pub_key).encode('utf-8'))
        return priv_key, pub_key

    def recv_textfile(self):
        path = input("Enter a path you would like to create a file in:\t")
        if check_files_path(path) == 'continue':
            try:
                f = open(path, 'w')
            except Exception as e:
                print("An error occurred")
            else:
                server_socket, client_socket = self.socket_operations()
                while True:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    print("From connected user:\t" + data)
                    priv_key, pub_key = self.create_keys()
                    f.write(decrypt(data, priv_key))
                    client_socket.send(data.encode('utf-8'))
            finally:
                f.close()
                self.sockets_close(server_socket, client_socket)

    @staticmethod
    def sockets_close(*args):
        for sock in args:
            sock.close()


class Client:
    def __init__(self, addr, host):
        self.addr = addr
        self.host = host

    def socket_operations(self):
        try:
            my_socket = socket.socket()
        except Exception as e:
            print("Socket could not be open! Check your network, Something went wrong in it")
            my_socket.close()
        else:
            my_socket.connect((self.addr, self.host))
            return my_socket

    def send_textfile(self, path):
        try:
            f = open(path, 'r')
        except FileNotFoundError as e:
            print(e)
        else:
            data = ''
            my_socket = self.socket_operations()
            chunk_size = 1024
            f_contents = f.read(chunk_size)
            while len(f_contents) > 0:
                my_socket.send(f_contents.encode('utf-8'))
                data += my_socket.recv(1024).decode('utf-8')
                f_contents = f.read(chunk_size)
            print("The server sent:\t" + data)
        finally:
            f.close()
            my_socket.close()

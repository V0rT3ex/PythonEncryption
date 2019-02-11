import Classes
from Classes import Server

def main():
   s = Server('127.0.0.1', 8820, 1)
   s.recv_textfile()


if __name__ == '__main__':
   main()


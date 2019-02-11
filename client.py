import Classes
from Classes import Client


def main():
   c = Client('127.0.0.1', 8820)
   c.send_textfile('text.txt')


if __name__ == '__main__':
   main()



import socket
import os
import sys

def main(s, addr):

    string = input("Alege un nume: ")
    s.sendto(string.encode(), addr)

    if os.fork() == 0:
        while 1:
            try:
                prop, addr = s.recvfrom(1024)
            except KeyboardInterrupt:
                sys.exit()
            if prop.decode() == "exit":
                sys.exit()

            print(prop.decode())

    while 1:
        string = input()
        s.sendto(string.encode(), addr)
        if string == "exit":
            break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass the port as the first argument!\n")
        sys.exit()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = "127.0.0.1"
        port = int(sys.argv[1])
        addr = (ip, port)
        main(s, addr)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        os.wait()
        print("La revedere!\n")
        s.sendto("exit".encode(), addr)
    finally:
        s.close()

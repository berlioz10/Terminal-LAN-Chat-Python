import socket
import sys

def main(s, arr):
    while 1:
        propozitie, addr = s.recvfrom(1024)
        if addr not in arr:
            print("S-a conectat " + str(addr) + " cu numele de " + propozitie.decode())
            print("Sunt " +str(len(arr) + 1)+ " utilizatori")
            addr = addr
            propozitie = propozitie.decode()
            arr[addr] = propozitie
            propozitie = "S-a conectat " + propozitie
            propozitie = propozitie.encode()
            for el in arr:
                if el != addr:
                    s.sendto(propozitie, el)
        else:
            propozitie = propozitie.decode()
            if propozitie == "exit":
                propozitie = arr[addr] + " s-a deconectat! ;-;"
                s.sendto("exit".encode(), addr)
                arr.pop(addr)
            else: 
                propozitie = arr[addr] + ": " + propozitie
            propozitie = propozitie.encode()
            for el in arr:
                if el != addr:
                    s.sendto(propozitie, el)

    s.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pass the port as the first argument!")
        sys.exit()
    try:
        arr = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', int(sys.argv[1])))
        main(s, arr)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        for el in arr:
            s.sendto("Se inchide serverul..".encode(), el)
            s.sendto("exit".encode(), el)
        print("Se inchide serverul..\n")
    finally:
        s.close()

# -*- coding: utf-8 -*-
__author__ = '22920172204299'
__date__ = '2019/11/06'

import socket
import threading


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('127.0.0.1', 9998)
    s.bind(addr)
    print('UDP Server on %s:%s...', addr[0], addr[1])

    user = {}  # {addr:name}
    while True:
        try:
            data, addr = s.recvfrom(1024)
            if not addr in user:
                if data.decode('utf-8') in user.values():
                    s.sendto('false'.encode(), addr)
                    continue
                else:
                    s.sendto('true'.encode(), addr)
                for address in user:
                    s.sendto(data + ' 进入聊天室...'.encode(), address)
                user[addr] = data.decode('utf-8')
                continue

            if 'EXIT' in data.decode('utf-8'):
                name = user[addr]
                user.pop(addr)
                for address in user:
                    s.sendto((name + ' 离开了聊天室...').encode(), address)
            else:
                print('"%s" from %s:%s' %
                      (data.decode('utf-8'), addr[0], addr[1]))
                for address in user:
                    if address != addr:
                        s.sendto(data, address)

        except ConnectionResetError:
            print('Someone left unexcept.')


if __name__ == '__main__':
    main()

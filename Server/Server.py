#!/usr/bin/env python3 1

import sys
import socket
import selectors
import traceback
import pyautogui as pg

import libServer
#
class Server():

    def __init__(self, port) -> None:
        self.sel = selectors.DefaultSelector()
        self.host = socket.gethostname()                           
        self.port = port
        self.message = None
        self._regeon = (0,0, pg.size()[0], pg.size()[1])

    def update_regeon(self, regeon):
        if self.message is None:
            self._regeon = regeon

        else:
            self.message.regeon = regeon
            self._regeon = regeon

        print("regeon Updated")

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        self.message = libServer.Message(self.sel, conn, addr, self._regeon)
        self.sel.register(conn, selectors.EVENT_READ, data=self.message)

    def Main(self, port):

        if port != None:
            self.port = port
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((self.host, self.port))
        lsock.listen()
        print(f"Listening on {(self.host, self.port)}")
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                f"Mai n: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            message.close()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

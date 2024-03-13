#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libClient

class Client:
    
    def __init__(self):

        self.sel = selectors.DefaultSelector()


    def create_request(self, action):
        if action != "":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action, encoding="utf-8"),
            )


    def start_connection(self, host, port, request):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libClient.Message(self.sel, sock, addr, request)
        self.sel.register(sock, events, data=message)


    def Main(self, action):
        print(action)
        host = "192.168.1.147"
        port = 4444
        action = action
        request = self.create_request(action)
        self.start_connection(host, port, request)

        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()



Client().Main(sys.argv[1])
#Client().Main("getText")
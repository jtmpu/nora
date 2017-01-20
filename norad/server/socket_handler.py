#!/usr/bin/env python
from .. import log
import ssl
import socket

class SocketHandler:
    '''
    Listens for new TCP connections, and handles the 
    TLS handshake. 
    On correct establishment of correction, lets
    a MessageHandler object handle the communication.
    '''
    def __init__(self, config, logger, message_handler):
        self.config = config
        self.logger = logger
        self.message_handler = message_handler
    
    def init(self):
        '''
        Set up SSL Contexts and socket settings
        '''
        self.logger.log("SocketHandler - initializing.", log.Debug)

        config_prot = self.config.get("security", "protocol")
        protocol = ssl.__dict__["PROTOCOL_"+config_prot]
        self.ssl_context = ssl.SSLContext(protocol)
        self.logger.log("SocketHandler - Using protocol: %s" % config_prot, log.Info)

        ciphers = self.config.get("security", "ciphers")
        self.ssl_context.set_ciphers(ciphers)
        self.logger.log("SocketHandler - Using ciphers: %s" % ciphers, log.Info)

        cafile = self.config.get("security", "cafile")
        self.ssl_context.load_verify_locations(cafile)
        self.logger.log("SocketHandler - Using CA File: %s" % cafile, log.Info)

        certificate = self.config.get("security", "certificate")
        key = self.config.get("security", "key")
        self.ssl_context.load_cert_chain(certificate, key)
        self.logger.log("SocketHandler - Using certificate file: %s" % certificate, log.Info)
        self.logger.log("SocketHandler - Using key file: %s" % key, log.Info)

        verify = self.config.get("security", "verify")
        if verify:
            self.ssl_context.verify_mode = ssl.CERT_REQUIRED
        else:
            self.ssl_context.verify_mode = ssl.CERT_NONE
        self.logger.log("SocketHandler - Verifying identities: %s" % verify, log.Info)

    def run(self):
        '''
        Runs the server
        '''
        self.logger.log("SocketHandler - Starting socket listener.", log.Debug)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = self.config.get("default", "ip")
        self.port = self.config.getint("default", "port")
        self.backlog = self.config.getint("default", "backlog")
        self.sock.bind((self.ip, self.port))
        self.sock.listen(self.backlog)
        self.logger.log("SocketHandler - Listening on: %s:%d" % (self.ip, self.port), log.Info)

        while True:
            client_socket,source = self.sock.accept()
            self.logger.log("SocketHandler - Accepted connection from %s:%d" % (source[0], source[1]), log.Info)

            try:
                ssl_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)     
            except Exception as e:
                self.logger.log("SocketHandler - TLS Exception: %s" % e, log.Error)
                client_socket.close()
                continue

            self.message_handler.handle_socket(ssl_socket)
	
            ssl_socket.shutdown(socket.SHUT_RDWR)
            ssl_socket.close()
            self.logger.log("SocketHandler - Closing connection from %s:%d" % (source[0], source[1]), log.Info)

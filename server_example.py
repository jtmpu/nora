#!/usr/bin/env python
import socket
import ssl

HOST="127.0.0.1"
PORT=9000
SSL_SERVER_KEY="server.key"
SSL_SERVER_CERTIFICATE="server.crt"
SSL_CA_FILE="ca.crt"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST,PORT))
sock.listen(1)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.set_ciphers("HIGH")
ssl_context.load_verify_locations(SSL_CA_FILE)
ssl_context.load_cert_chain(SSL_SERVER_CERTIFICATE, SSL_SERVER_KEY)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = False
ssl_context.options &= ~ssl.OP_NO_SSLv3
ssl_context.options &= ~ssl.OP_NO_SSLv2
ssl_context.options &= ~ssl.OP_NO_TLSv1


while True:
	try:
		client_sock,_ = sock.accept()	
		ssl_sock = ssl_context.wrap_socket(client_sock, server_side=True)
	
		ssl_sock.close()	
	except:
		continue

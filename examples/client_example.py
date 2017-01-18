#!/usr/bin/env python
import socket
import ssl

HOST="127.0.0.1"
PORT=17341

SSL_CLIENT_KEY="../certs/example_client.key"
SSL_CLIENT_CERTIFICATE="../certs/example_client.crt"
SSL_CA_FILE="../certs/example_ca.crt"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_verify_locations(SSL_CA_FILE)
ssl_context.set_ciphers("ECDHE-RSA-AES256-GCM-SHA384")
ssl_context.load_cert_chain(SSL_CLIENT_CERTIFICATE, SSL_CLIENT_KEY)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = False
ssl_context.options &= ~ssl.OP_NO_SSLv3
ssl_context.options &= ~ssl.OP_NO_SSLv2
ssl_context.options &= ~ssl.OP_NO_TLSv1

ssl_sock = ssl_context.wrap_socket(sock)
ssl_sock.connect((HOST, PORT))

print("Connected successfully!")
ssl_sock.close()

#!/usr/bin/env python
import ConfigParser
import os
import socket
import ssl

DEFAULT_CONFIG_NAME="norad_default.cfg"
OVERRIDE_CONFIG_NAME="norad.cfg"

config = ConfigParser.ConfigParser()
with open(DEFAULT_CONFIG_NAME, "r") as f:
    config.readfp(open(DEFAULT_CONFIG_NAME))
if os.path.exists(OVERRIDE_CONFIG_NAME):
    with open(OVERRIDE_CONFIG_NAME, "r") as f:
        config.readfp(open(OVERRIDE_CONFIG_NAME))

# Check for dangerous configuration
default = ConfigParser.ConfigParser()
with open(DEFAULT_CONFIG_NAME, "r") as f:
    default.readfp(open(DEFAULT_CONFIG_NAME))

if (config.get("security", "cafile") == default.get("security", "cafile")
    and config.get("security", "certificate") == default.get("security", "certificate")
    and config.get("security", "key") == default.get("security", "key")):
    # Default certificates are used in the application
    print("********** WARNING ***********")
    print(" IT IS NOT RECOMMENDED TO USE ")
    print("   THE EXAMPLE CERTIFICATES ")
    print("******************************")
    print("[!] WARNING - DEFAULT CERTIFICATES")
if not config.getboolean("security", "verify"):
    print("[!] WARNING - CERT VERIFICATION DISABLED")
    

# Setup strict SSL Context
config_prot = config.get("security", "protocol")
protocol = ssl.__dict__["PROTOCOL_"+config_prot]

ssl_context = ssl.SSLContext(protocol)
ssl_context.set_ciphers(config.get("security", "ciphers"))
print(config.get("security", "ciphers"))
ssl_context.load_verify_locations(config.get("security", "cafile"))
ssl_context.load_cert_chain(config.get("security", "certificate"),
                            config.get("security", "key"))
if config.getboolean("security", "verify"):
    ssl_context.verify_mode = ssl.CERT_REQUIRED
else:
    ssl_context.verify_mode = ssl.CERT_NONE

# Setup socket listener
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = config.get("default", "ip")
port = config.getint("default", "port")
backlog = config.getint("default", "backlog")
sock.bind((ip, port))
sock.listen(1)
print("[+] Listening on (%s, %d)." % (ip, port))

# Wait for clients
while True:
    try: 
        client,_ = sock.accept()
        print("[+] Client connected")
        ssl_socket = ssl_context.wrap_socket(client, server_side=True)
        ssl_socket.close()
        print("[+] Client disconnected")
    except KeyboardInterrupt as e:
        print("[-] Shutting down.")
        break
    except Exception as e:
        print("[-] Error in handshake: %s" % e)

print("[+] Closing.")
sock.close()

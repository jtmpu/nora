#!/usr/bin/env python
import json

from .. import log

class MessageHandler:

    def __init__(self, config, logger):
        '''
        Initializes the message handler
        '''
        self.logger = logger
        self.buffer_size = config.getint("network", "buffersize")
        logger.log("MessageHandler - Setup done.", log.Info)

    def handle_socket(self, socket):
        '''
        Communicates with the client, and ensure messages
        are handled correctly.
        '''
        request = socket.recv(self.buffer_size)
        error = {
                  "result_code" : 503,
                  "result_msg" : "Internal Server Error",
                  "meta" : [],
                  "data" : "Not implemented"
                }
        response = json.dumps(error)
        socket.send(response)
        return True

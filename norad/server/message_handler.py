#!/usr/bin/env python
import json

from .. import log

class MessageHandler:
    '''
    Handles the communication with the client and the 
    support plugins of the NORA daemon.

    Enforces that requests are properly formatted and 
    are targeting valid commands.
    Otherwise; returns errors to clients. 
    '''
    def __init__(self, factory):
        '''
        Initializes the message handler
        '''
        self.logger = factory.get_logger()
        self.buffer_size = factory.get_config().getint("network", "buffersize")
        self.module_handler = factory.create_module_handler()
        self.logger.log("MessageHandler - Setup done.", log.Info)

    def handle_socket(self, socket):
        '''
        Communicates with the client, and ensure messages
        are handled correctly.
        '''
        request = ""
        received = self.buffer_size
        while received == self.buffer_size:
            tmp = socket.recv(self.buffer_size)
            received = len(tmp)
            request += tmp


        json_request = {}
        try:
            json_request = json.loads(request)
        except Exception as e:
            self.logger.log("MessageHandler - Failed to deserialize JSON: %s" % request, log.Error)
            self.respond_error(socket, 500, "The request was not formatted properly.", [], "")
            return False

        if ("command" not in json_request 
           or "meta" not in json_request 
           or "data" not in json_request):
           # Incorrect format of the JSON request
            self.respond_error(socket, 500, "The request was not formatted properly.", [], "")
            return False

        if json_request["command"] not in self.module_handler.get_modules().keys():
            # Command not found
            self.respond_error(socket, 501, "The command %s is not a recognized command." % json_request["command"], [], "See help for available commands.")
            return False

        module = self.module_handler.get_modules()[json_request["command"]]
        if not module.is_valid_request(json_request):
            # Command does finds the arguments to be incorrect
            self.respond_error(socket, 502, "Request data is not valid.", [], "Check help <command_name>")
            return False

        try:
            response_data = module.process_request(json_request)
        except Exception as e:
            self.logger.log("MessageHandler - Error when performing command. Error: %s" % e.message, log.Error)
            self.respond_error(socket, 503, "Internal Server Error", [], e.message)
            return False
            

        result = {
                   "result_code" : 200,
                   "result_msg" : "Success.",
                   "meta" : [],
                   "data" : response_data
                 }

        response = json.dumps(result)
        socket.send(response)
        return True

    def respond_error(self, socket, code, msg, meta, data):
        error = { "error_code" : code, "result_msg" : msg, "meta" : meta, "data" : data }
        response = json.dumps(error)
        socket.send(response)

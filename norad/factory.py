#!/usr/bin/env python

from . import log
from .server import socket_handler
from .server import message_handler
from .modules import module_handler
from .modules import add_note

class Factory:
    def __init__(self, config):
        self.config = config
        self.logger = None

    def get_config(self):
        return self.config

    def get_logger(self):
        if self.logger == None:
            self.logger = log.Logger(self.config)
        return self.logger

    def create_messagehandler(self):
        return message_handler.MessageHandler(self)

    def create_sockethandler(self):
        return socket_handler.SocketHandler(self.config, self.get_logger(), 
                                            self.create_messagehandler())
    def create_module_handler(self):
        return module_handler.ModuleHandler(self)

    def create_module_add_note(self):
        return add_note.AddNote(self)

FACTORY_SINGLETON = None
def create_factory(config):
    global FACTORY_SINGLETON
    FACTORY_SINGLETON = Factory(config)
    return FACTORY_SINGLETON

def get_factory():
    return FACTORY_SINGLETON

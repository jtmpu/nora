#!/usr/bin/env python

from . import log
from .server import socket_handler
from .server import message_handler

class Factory:
    def __init__(self, config):
        self.config = config
        self.logger = None

    def get_logger(self):
        if self.logger == None:
            self.logger = log.Logger(self.config)
        return self.logger

    def create_messagehandler(self):
        return message_handler.MessageHandler(self.config, self.get_logger())

    def create_sockethandler(self):
        return socket_handler.SocketHandler(self.config, self.get_logger(), 
                                            self.create_messagehandler())

FACTORY_SINGLETON = None
def create_factory(config):
    global FACTORY_SINGLETON
    FACTORY_SINGLETON = Factory(config)
    return FACTORY_SINGLETON

def get_factory():
    return FACTORY_SINGLETON

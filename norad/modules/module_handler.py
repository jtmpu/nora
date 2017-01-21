#!/usr/bin/env python

class ModuleHandler:
    '''
    Handles all available modules of the server.
    One module is capable of handling one type of request.

    One crazy feature of the ModuleHandler is that it is actually a
    module itself, 

    A moodule has the following capabilities:
        - module.get_command()
            * Returns the associated command name.
        - module.get_description()
            * Returns a short description of the module.
        - module.process_request(request)
            * Handles the request, and returns response data
        - module.is_valid_request(request)
            * Checks that the module is capable of handling the request
    '''
    def __init__(self, factory):
        self.config = factory.get_config()
        self.modules = {}

        # ModuleHandler is also the Help module, talk about too much responsibility
        self.modules[self.get_command()] = self

        add_note = factory.create_module_add_note()
        self.modules[add_note.get_command()] = add_note

    def get_command(self):
        return "help"

    def get_description(self):
        return "Use help <command> for more information about a specific command.\n"  

    def is_valid_request(self, request):
        return True

    def process_request(self, request):
        '''
        Return the help message containing available modules
        and descriptions
        ''' 
        if request["data"] == "":
            # Return list of available commands
            response = self.get_description()
            response += "\nAvailable commands:\n"
            for command in self.modules.keys():
                response += " - " + command + "\n"
            return response
        elif request["data"] in self.modules:
            return self.modules[request["data"]].get_description()
        else:
            raise Exception("Command not recognized")

    def get_modules(self):
        '''
        Returns a dict with the commands as shown below:
            modules['<command_name>'] = module_object
        '''
        return self.modules

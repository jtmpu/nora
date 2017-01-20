#!/usr/bin/env python
import os

Debug, Info, Warning, Error = ("[DEBUG]", "[INFO]", "[WARNING]", "[ERROR]")
class Logger:
    def __init__(self, config):
        '''
        Sets up the log object
        '''
        self.path = config.get("log", "path")
        self.use_console = config.getboolean("log", "stdout")

        if not self.use_console:
            if not os.path.exists(self.path):
            	with open(self.path, "w") as f:
               	 f.write("[+] Created log file.\n")

    def log(self, msg, level):
        if self.use_console:
            print("%s %s" % (level, msg))
        else:
            with open(self.path, "a") as f:
                f.write("%s %s\n" % (level, msg))

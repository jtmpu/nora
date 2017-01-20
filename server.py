#!/usr/bin/env python
import os
import ConfigParser

import norad.log
import norad.factory


DEFAULT_CONFIG_NAME="norad_default.cfg"
OVERRIDE_CONFIG_NAME="norad.cfg"

config = ConfigParser.ConfigParser()
with open(DEFAULT_CONFIG_NAME, "r") as f:
    config.readfp(open(DEFAULT_CONFIG_NAME))
if os.path.exists(OVERRIDE_CONFIG_NAME):
    with open(OVERRIDE_CONFIG_NAME, "r") as f:
        config.readfp(open(OVERRIDE_CONFIG_NAME))

factory = norad.factory.create_factory(config)
logger = factory.get_logger()

# Check for dangerous configuration
default = ConfigParser.ConfigParser()
with open(DEFAULT_CONFIG_NAME, "r") as f:
    default.readfp(open(DEFAULT_CONFIG_NAME))

if (config.get("security", "cafile") == default.get("security", "cafile")
    and config.get("security", "certificate") == default.get("security", "certificate")
    and config.get("security", "key") == default.get("security", "key")):
    # Default certificates are used in the application
    logger.log("DEFAULT CERTIFICATES USED.", norad.log.Warning)
if not config.getboolean("security", "verify"):
    logger.log("CERTIFICATE VERIFICATION DISABLED", norad.log.Warning)



socket_handler = factory.create_sockethandler()
socket_handler.init()
socket_handler.run()

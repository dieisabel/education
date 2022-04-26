"""Module for configuration"""

import socket
import logging


SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8000

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(name)s: %(message)s"
)

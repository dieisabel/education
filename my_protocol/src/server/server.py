"""Module for simple TCP server"""

__all__ = ['TcpServer']

import logging
import typing
import socket
from socket import socket as Socket

from layers.presentation import CanPresent
from layers.presentation import PresentationLayer


class Server:
    """Simple TCP server

    Can work only with one connection at the moment

    Attributes:
        ipv4: IPv4 address
        port: Port
        buffer_size: Maximum size of receiving data in bytes
        stop_word: Stop word to break connection
    """

    def __init__(
        self,
        ipv4: str,
        port: int,
        buffer_size: int = 64,
        stop_word: str = "STOP",
    ) -> None:
        self.socket = Socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ipv4 = ipv4
        self.port = port
        self.buffer_size = buffer_size
        self.stop_word = stop_word
        self.presentation_layer: CanPresent = PresentationLayer()

        self.logger = logging.getLogger()

    def start(self) -> None:
        """Start server"""

        self.socket.bind((self.ipv4, self.port))
        self.socket.listen(1)
        self.logger.info(f"Server start on {self.ipv4}:{self.port}")

        while True:
            connection, client_address = self.socket.accept()
            self._handle_client(connection, client_address)

        self.logger.info(f"Server down on {self.ipv4}:{self.port}")

    def _handle_client(self, connection: Socket, client_address: typing.Tuple[str]) -> None:
        """Handle client connection

        Args:
            connection: Socket the client is connected to
            client_address: Client address represented as a tuple, where
                            first element - ip address, second - port

        Returns:
            None
        """

        self.logger.info(f"{client_address[0]}:{client_address[1]} connected")

        while True:
            data = self._receive_data(connection)
            self.logger.info(f"Received \"{data}\" from {client_address[0]}:{client_address[1]}")

            if data == self.stop_word:
                self._send_data(connection, "Bye, bye!")
                connection.close()
                break

            self._send_data(connection, data)

        self.logger.info(f"Drop connection from {client_address[0]}:{client_address[1]}")

    def _receive_data(self, connection: Socket) -> str:
        """Receive data from socket and decode it

        Args:
            connection: Socket the client is connected to

        Returns:
            Decoded data

        Note:
            Maximum size of data that can be received is determined by buffer_size
        """

        data: bytes = connection.recv(self.buffer_size)
        return self.presentation_layer.present_data(data)

    def _send_data(self, connection: Socket, data: str) -> None:
        """Send data using socket

        Args:
            connection: Socket the client is connected to
            data: Data to send

        Returns:
            None
        """

        connection.send(self.presentation_layer.prepare_data(data))

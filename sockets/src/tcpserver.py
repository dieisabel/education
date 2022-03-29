"""Module for simple TCP server"""

__all__ = ['TcpServer']

import logging
from typing import Union
from typing import Tuple
from socket import socket as Socket
from socket import AF_INET
from socket import SOCK_STREAM


logging.basicConfig(level=logging.DEBUG)


class TcpServer:
    """Simple TCP server

    Can work only with one connection at the moment

    Attributes:
        ipv4: IPv4 address
        port: Port
        buffer_size: Maximum size of receiving data in bytes
        encoding: Data encoding
        stop_word: Stop word to break connection
    """

    def __init__(
        self,
        ipv4: str,
        port: int,
        buffer_size: int = 64,
        encoding: str = "utf-8",
        stop_word: str = "STOP",
    ) -> None:
        self.__socket = Socket(AF_INET, SOCK_STREAM)

        self._ipv4 = ipv4
        self._port = port
        self._buffer_size = buffer_size
        self._encoding = encoding
        self._stop_word = stop_word

        self._logger = logging.getLogger()

    def start(self) -> None:
        """Start server"""

        self.__socket.bind((self._ipv4, self._port))
        self.__socket.listen(1)
        self._logger.info(f"Server start on {self._ipv4}:{self._port}")

        while True:
            connection, client_address = self.__socket.accept()
            self._handle_client(connection, client_address)

        self._logger.info(f"Server down on {self._ipv4}:{self._port}")

    def _handle_client(self, connection: Socket, client_address: Tuple[str]) -> None:
        """Handle client connection

        Args:
            connection: Socket the client is connected to
            client_address: Client address represented as a tuple, where
                            first element - ip address, second - port

        Returns:
            None
        """

        self._logger.info(f"{client_address[0]}:{client_address[1]} connected")

        while True:
            data = self._receive_data(connection)
            self._logger.info(
                f"Received \"{data}\" from {client_address[0]}:{client_address[1]}"
            )

            if data == self._stop_word:
                self._send_data(connection, "Bye, bye!")
                connection.close()
                break

            self._send_data(connection, data)

        self._logger.info(
            f"Drop connection from {client_address[0]}:{client_address[1]}"
        )

    def _receive_data(self, connection: Socket) -> str:
        """Receive data from socket and decode it

        Args:
            connection: Socket the client is connected to

        Returns:
            Decoded data

        Note:
            Maximum size of data that can be received is determined by buffer_size
        """

        return connection.recv(self._buffer_size).decode(self._encoding)

    def _send_data(self, connection: Socket, data: Union[str, bytes]) -> None:
        """Send data using socket

        Args:
            connection: Socket the client is connected to
            data: Data to send

        Returns:
            None
        """

        if isinstance(data, str):
            connection.send(data.encode(self._encoding))
        else:
            connection.send(data)

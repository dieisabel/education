"""Module for presentation layer"""

__all__ = [
    "CanPresent",
    "PresentationLayer",
]

import typing
import gzip


class CanPresent(typing.Protocol):
    """Protocol for presentation layer

    Object can prepare data for transmittion over network or represent data from bytes
    """

    def prepare_data(self, data: str) -> bytes:
        """Prepare data to be send

        Args:
            data: Data to send

        Returns:
            Prepared to sending data
        """

    def represent_data(self, bytecode: bytes) -> str:
        """Represent data from bytes

        Args:
            bytedata: Data in bytes

        Returns:
            Decoded data
        """


class PresentationLayer:
    """Presentation layer implementation

    The presentation layer (data presentation layer, data provision level) sets the
    system-dependent representation of the data (for example, ASCII, EBCDIC) into an
    independent form, enabling the syntactically correct data exchange between different systems

    For compression layer is using gzip library

    Attributes:
        encoding: Data encoding
        compression_level: An integer from 0 to 9 that controlls the level of compression; 1 is
            fastest and produces the least compression, and 9 is slowest and produces the
            most compression
    """

    def __init__(self, encoding: str = "utf-8", compression_level: int = 1) -> None:
        self.encoding = encoding
        self.compression_level = compression_level

    def prepare_data(self, data: str) -> bytes:
        """Prepare data to be send through network

        Data preparing implemented in 2 steps:
        1. Encoding data in self.encoding encoding
        2. Compressing using gzip library

        Args:
            data: Data to send

        Returns:
            Prepared to sending data
        """

        encoded_data: bytes = data.encode(self.encoding)
        return gzip.compress(encoded_data, compresslevel=self.compression_level)

    def represent_data(self, bytedata: bytes) -> str:
        """Represent data from bytes

        Get data from bytes. Implemented in 2 steps:
        1. Uncompress data using gzip library
        2. Decode data

        Args:
            bytedata: Data in bytes

        Returns:
            Decoded data
        """

        uncompressed_data: bytes = gzip.decompress(bytedata)
        return uncompressed_data.decode(self.encoding)

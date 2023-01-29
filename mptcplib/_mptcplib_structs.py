from typing import Tuple
import struct

class MptcplibStructInterface:
    _format: str 

    def size():  ...

    @property
    def value(*args) -> any: ...

class MptcplibStruct(MptcplibStructInterface):
    
    def __init__(self, format: str, *init_values) -> None:
        self._bytes_object = struct.pack(format, *init_values)
    
    @classmethod
    def size(cls):
        return struct.calcsize(cls._format)     

    @classmethod
    def decode(cls, buffer: bytes) -> MptcplibStructInterface:
        values = struct.unpack(cls._format, buffer)
        return cls(values)


class BooleanStruct(MptcplibStruct):
    _format = "?"

    def __init__(self, init_values: Tuple[bool] = False) -> None:
        super().__init__(BooleanStruct._format, init_values)
    
    @property
    def value(self) -> bool:
        return struct.unpack(BooleanStruct._format, self._bytes_object)[0]
from typing import Tuple
import struct
import socket

try:
    IPPROTO_MPTCP = socket.IPPROTO_MPTCP
except AttributeError:
    IPPROTO_MPTCP = 262

try:
    SOL_MPTCP = socket.SOL_MPTCP
except AttributeError:
    SOL_MPTCP = 284

try: 
    MPTCP_INFO = socket.MPTCP_INFO
except AttributeError:
    MPTCP_INFO = 1

try: 
    MPTCP_TCPINFO = socket.MPTCP_TCPINFO
except AttributeError:
    MPTCP_TCPINFO = 2

class MptcplibStructInterface:
    _format: str 

    def size() -> int:  ...

    @property
    def value(*args) -> any: ...

class MptcplibStruct(MptcplibStructInterface):
    _format = "X" # Pad type, there's no value associated
    
    def __init__(self, format: str, init_values) -> None:
        print(init_values)
        self._bytes_object = struct.pack(format, *init_values)
    
    @classmethod
    def size(cls):
        return struct.calcsize(cls._format)

    @classmethod
    def decode(cls, buffer: bytes) -> MptcplibStructInterface:
        values = struct.unpack(cls._format, buffer)
        return cls(values)

class MptcpSubflowDataStruct(MptcplibStruct):
    """The struct for the C 'struct mptcp_subflow_data'

    struct mptcp_subflow_data {
        __u32		size_subflow_data;		/* size of this structure in userspace */
        __u32		num_subflows;			/* must be 0, set by kernel */
        __u32		size_kernel;			/* must be 0, set by kernel */
        __u32		size_user;				/* size of one element in data[] */
    } __attribute__((aligned(8)));
    """
    _format = "=IIII" # We use the '=' meaning none alignement and standard sizes

    def __init__(self, init_values: Tuple[int] = (0,0,0,0)) -> None:
        if len(init_values) != 4:
            raise AttributeError(f"init_values tuple given to the BooleanStruct contructor should be of length 1:"\
                                 f"got {init_values} of lenght: {len(init_values)}")
        super().__init__(MptcpSubflowDataStruct._format, init_values)
    
    @property
    def value(self) -> Tuple[int]:
        """Returns a tuple of values of the struct as specified in the class description the same order.

        :return: A tuple of ints (size_subflow_data, num_subflows, size_kernel, size_user)
        :rtype: Tuple[int]
        """
        return struct.unpack(MptcpSubflowDataStruct._format, self._bytes_object)

    @property
    def size_subflow_data(self) -> int:
        return self.value[0]

    @property
    def num_subflows(self) -> int:
        return self.value[1]
    
    @property
    def size_kernel(self) -> int:
        return self.value[2]
    
    @property
    def size_user(self) -> int:
        return self.value[3]
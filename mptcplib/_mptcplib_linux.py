import socket
import ctypes
import os

from ._common_constants import *

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

try:
    import ctypes

    # distinct socklen_t type
    class socklen_t(ctypes.c_uint32):
        pass

    class mptcp_subflow_data(ctypes.Structure):
        _fields_ = (
            ('size_subflow_data', ctypes.c_uint32), # this structure size
            ('num_subflows', ctypes.c_uint32),      # must be 0
            ('size_kernel', ctypes.c_uint32),       # must be 0
            ('size_user', ctypes.c_uint32),         # element size in data[]
        )

        def __init__(self, size_user=0):
            super().__init__(size_user=size_user)
            self.size_subflow_data = ctypes.sizeof(self)

    getsockopt = ctypes.CDLL(None, use_errno=True).getsockopt
    getsockopt.restype = ctypes.c_int
    getsockopt.argtypes = (
        ctypes.c_int,      # sockfd
        ctypes.c_int,      # level
        ctypes.c_int,      # optname
        ctypes.c_void_p,   # optval
        ctypes.POINTER(socklen_t), # optlen
    )

except (ImportError, TypeError, AttributeError):
    getsockopt = None

def _linux_get_nb_used_subflows(sock: socket.socket) -> int:
    if getsockopt == None:
        raise NotImplementedError("The operation is not supported on your OS.")
    optval = mptcp_subflow_data()
    optlen = socklen_t(ctypes.sizeof(optval))
    if getsockopt(  sock.fileno(), SOL_MPTCP, 2, 
                    ctypes.byref(optval), ctypes.byref(optlen)) == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return optval.num_subflows
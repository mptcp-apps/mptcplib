""" Interface module
Servers as the interface of the user. 
"""
from sys import platform
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

_os_supports_mptcp = True

IS_LINUX = platform.startswith("linux")

from . import _mptcplib_linux as ext_linux
from ._utils import _linux_required_kernel, _linux_get_sysfs_variable
from ._mptcplib_structs import *

def socket_is_mptcp(sock: socket.socket):
    if IS_LINUX and _linux_required_kernel("5.16"):
        return_bytes = sock.getsockopt(SOL_MPTCP, MPTCP_INFO, BooleanStruct.size())
        return BooleanStruct.decode(return_bytes).value

    # If it reaches then the operation is not supported on the Host OS
    raise NotImplementedError("The operation is not supported on your OS.")

def used_subflows(sockfd):
    if (IS_LINUX or platform == "linux2") and _linux_required_kernel("5.16"):
        return ext_linux.used_subflows(sockfd)
    
    # If it reaches then the operation is not supported on the Host OS
    raise NotImplementedError("The operation is not supported on your OS.")

def create_mptcp_socket(family_type, sock_type):
    global _os_supports_mptcp
    if _os_supports_mptcp and sock_type == socket.SOCK_STREAM:
        try:
            return socket.socket(family_type, socket.SOCK_STREAM, IPPROTO_MPTCP)
        except socket.error as e:
            pass
    # Multipath TCP does not work or socket failed, we try TCP
    return socket.socket(family_type, sock_type, socket.IPPROTO_TCP)

def is_mptcp_enabled_and_supported():
    global _os_supports_mptcp
    if IS_LINUX and _linux_required_kernel("5.6"):
        _os_supports_mptcp = _linux_get_sysfs_variable("net.mptcp.enabled") == "1"
        return _os_supports_mptcp

    # The OS doesn't support MPTCP
    _os_supports_mptcp = False
    return False
""" Interface module
"""
import socket
import errno

_os_supports_mptcp = True

from ._common_constants import *
from ._mptcplib_linux import (
    _linux_get_nb_used_subflows, 
    _linux_is_socket_mptcp, 
    IS_LINUX,
    _linux_is_mptcp_supported, 
    _linux_is_mptcp_enabled,
)

def is_socket_mptcp(sock: socket.socket):
    if IS_LINUX:
        return _linux_is_socket_mptcp(sock) 
    # If it reaches here then the operation is not supported on the host OS
    raise NotImplementedError("The operation is not supported on your OS.")

def get_nb_used_subflows(sock: socket.socket):
    if IS_LINUX:
        return _linux_get_nb_used_subflows(sock)
    # If it reaches here then the operation is not supported on the host OS
    raise NotImplementedError("The operation is not supported on your OS.")

def create_mptcp_socket(family_type, sock_type):
    if is_mptcp_enabled_and_supported() and sock_type == socket.SOCK_STREAM:
        try:
            return socket.socket(family_type, socket.SOCK_STREAM, IPPROTO_MPTCP)
        except socket.error as e:
            pass
    # Multipath TCP does not work or socket failed, we try standard TCP initialisation
    return socket.socket(family_type, sock_type, socket.IPPROTO_TCP)

def _is_mptcp_supported():
    global _os_supports_mptcp
    if not _os_supports_mptcp:
        return False
    if IS_LINUX:
        return _linux_is_mptcp_supported()
    # If reaches here then host OS doesn't support MPTCP
    _os_supports_mptcp = False
    return False 

def is_mptcp_enabled_and_supported():
    if IS_LINUX:
        return _linux_is_mptcp_enabled() and _linux_is_mptcp_supported()
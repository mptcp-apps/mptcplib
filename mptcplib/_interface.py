""" Interface module
Servers as the interface of the user. 
"""
from sys import platform
import socket
import errno

_os_supports_mptcp = True
IS_LINUX = platform.startswith("linux") or platform == "linux2" 

from . import _mptcplib_linux as ext_linux

from ._utils import _linux_required_kernel, _linux_get_sysfs_variable
from ._mptcplib_structs import *

def socket_is_mptcp(sock: socket.socket):
    if IS_LINUX and _linux_required_kernel("5.16"):
        if not _is_mptcp_enabled():
            return False
        try:
            _ = sock.getsockopt(SOL_MPTCP, MPTCP_INFO, 1)
            # If no error occurs then it's MPTCP, not fan of using error handling as a execution flow
            # but it's the current way to hande fallbacks to TCP.
            # c.f https://github.com/multipath-tcp/mptcp_net-next/issues/294#issuecomment-1301920288 */
            return True 
        except OSError as error:
            if error.args[0] != errno.EOPNOTSUPP:
                raise
            return False

    # If it reaches here then the operation is not supported on the host OS
    raise NotImplementedError("The operation is not supported on your OS.")

def used_subflows(sock: socket.socket):
    if IS_LINUX and _linux_required_kernel("5.16"):
        if not socket_is_mptcp(sock):
            return -1
        subflow_data: MptcpSubflowDataStruct = MptcpSubflowDataStruct.decode(sock.getsockopt(SOL_MPTCP, MPTCP_TCPINFO, MptcpSubflowDataStruct.size()))
        return subflow_data.num_subflows
    
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

def _is_mptcp_enabled():
    return _linux_get_sysfs_variable("net.mptcp.enabled") == "1"

def _is_mptcp_supported():
    global _os_supports_mptcp

    if not _os_supports_mptcp:
        return False

    if IS_LINUX and _linux_required_kernel("5.6"):
        return _is_mptcp_enabled()

    # If reaches here then host OS doesn't support MPTCP
    _os_supports_mptcp = False
    return False 

def is_mptcp_enabled_and_supported():
    return _is_mptcp_enabled() and _is_mptcp_supported()
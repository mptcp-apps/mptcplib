import socket
""" Stub file of all the function in the public interface
"""

IPPROTO_MPTCP: int 
__version__: str

def socket_is_mptcp(fd: int) -> bool:
    """Checks if the socket identified by the given file descriptor is a 
    MPTCP socket.

    :param fd: File descriptor of the socket.
    :type fd: int
    :raises mptcplib.error: If the file descriptor is less or equal to zero or an error occured.
    :raises NotImplementedError: If the operation is not supported on the host OS.
    :return: Boolean indicating if the socket is MPTCP
    :rtype: bool
    """ 
    ...

def used_subflows(fd: int) -> int:
    """Returns the number of subflows used by the connection

    :param fd: File descriptor of a MPTCP socket
    :type fd: int
    :raises mptcplib.error: Indicating the errno code.
    :raises NotImplementedError: If the operation is not supported on the host OS.
    :return: -1 if fallback to TCP, -2 if the operation isn't supported else the number of used subflows.
    :rtype: int
    """
    ...

def create_mptcp_socket(family_type: socket.AddressFamily, sock_type: socket.SocketKind) -> socket.socket:
    """Tries to make a MPTCP socket if the system supports MPTCP and the socktype is SOCK_STREAM
    else it creates a normal TCP socket.

    :param family_type: Python socket address family.
    :type family_type: socket.AddressFamily.
    :param sock_type: Socket type.
    :type sock_type: socket.SocketKind.
    :return: a socket that is maybe MPTCP depending on OS and if MPTCP is enabled.
    :rtype: socket.socket
    """
    ...

def is_mptcp_enabled_and_supported() -> bool:
    """Checks if mptcp is supported on host OS and if possible it is enabled

    :return: The boolean indicating if mptcp is supported and enabled.
    :rtype: bool
    """
    ...
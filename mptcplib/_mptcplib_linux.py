import socket
import ctypes
import os
import subprocess
from sys import platform
import errno

from ._common_constants import *
IS_LINUX = platform.startswith("linux")

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

def _linux_get_sysfs_variable(variable):
    cmd_result, _ = subprocess.Popen(["sysctl", variable], stdout=subprocess.PIPE, stderr=None).communicate()
    return cmd_result.decode('utf-8').split("=")[1].strip()

def _linux_is_mptcp_enabled():
    return _linux_get_sysfs_variable("net.mptcp.enabled") == "1"

def _linux_required_kernel(expected_release):
    return _linux_compare_kernel_version(_get_linux_kernel_version(), expected_release) >= 0

def _linux_is_socket_mptcp(sock: socket.socket):
    # c.f https://github.com/multipath-tcp/mptcp_net-next/issues/294#issuecomment-1301920288 */
    if not _linux_required_kernel("5.6"):
        return False
    if not _linux_is_mptcp_enabled():
        return False
    if getsockopt == None:
        raise NotImplementedError("The operation not supported on Host OS.")
    optval = ctypes.c_bool()
    optlen = socklen_t(ctypes.sizeof(ctypes.c_bool))
    if getsockopt(  sock.fileno(), SOL_MPTCP, MPTCP_INFO, 
                    ctypes.byref(optval), ctypes.byref(optlen) ) == -1:
        err_no = ctypes.get_errno()
        if err_no == errno.EOPNOTSUPP:
            return False
        raise OSError( err_no, os.strerror(err_no) )
    return True

def _linux_get_nb_used_subflows(sock: socket.socket) -> int:
    if not _linux_required_kernel("5.16") or getsockopt == None:
        raise NotImplementedError("The operation requires a kernel >= 5.16")
    if not _linux_is_socket_mptcp(sock):
        return -1
    optval = mptcp_subflow_data()
    optlen = socklen_t(ctypes.sizeof(optval))
    if getsockopt(  sock.fileno(), SOL_MPTCP, MPTCP_TCPINFO, 
                    ctypes.byref(optval), ctypes.byref(optlen)) == -1:
        err_no = ctypes.get_errno()
        raise OSError( err_no, os.strerror(err_no) )
    return optval.num_subflows

def _get_linux_kernel_version():
    cmd_result, _ = subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE, stderr=None).communicate()
    return cmd_result.decode("utf-8")

def _linux_compare_kernel_version(this_version, other_version):
    this_to_array, other_to_array = this_version.split('.')[:2], other_version.split('.')[:2]
    min_length = min(len(this_to_array), len(other_to_array))
    for idx in range(min_length):
        this_to_number  = int(this_to_array[idx])
        other_to_number = int(other_to_array[idx])
        if   this_to_number < other_to_number:
            return -1
        elif this_to_number > other_to_number:
            return 1
    return 0

def _linux_is_kernel_module_installed(module_name):
    lsmod_proc = subprocess.Popen(["modinfo", module_name], stdout=subprocess.PIPE, stderr=None)
    lsmod_proc.communicate()
    return lsmod_proc.returncode == 0

def _linux_is_mptcp_supported():
    return _linux_required_kernel("5.6") and _linux_is_kernel_module_installed("mptcp_diag")
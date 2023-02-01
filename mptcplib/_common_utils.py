"""
Utility module 
"""
import subprocess

def _get_linux_kernel_version():
    cmd_result, _ = subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE, stderr=None).communicate()
    return cmd_result.decode("utf-8")

def _linux_compare_kernel_version(this_version, other_version):
    this_to_array, other_to_array = this_version.split('.')[:2], other_version.split('.')[:2]
    min_length = min(len(this_to_array), len(other_to_array))
    for idx in range(min_length):
        this_to_number = int(this_to_array[idx])
        other_to_number = int(other_to_array[idx])
        if  this_to_number < other_to_number:
            return -1
        elif this_to_number > other_to_number:
            return 1
    return 0

def _linux_required_kernel(expected_release):
    return _linux_compare_kernel_version(_get_linux_kernel_version(), expected_release)>= 0

def _linux_get_sysfs_variable(variable):
    cmd_result, _ = subprocess.Popen(["sysctl", variable], stdout=subprocess.PIPE, stderr=None).communicate()
    return cmd_result.decode('utf-8').split("=")[1].strip()
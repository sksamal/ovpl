# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" A module for managing VMs on CentOS - OpenVZ platform. """

__all__ = [
    'create_VM',
    'restart_VM',
    'start_VM_manager',
    'stop_VM',
    'destroy_VM',
    'is_running_VM',
    'migrate_VM',
    'take_snapshot',
    'InvalidVMIDException',
    ]

# Standard Library imports
import re
import subprocess
from exceptions import Exception

# Third party imports
import netaddr

# VLEAD imports
import VMSpec
import VMUtils

# UGLY DUCK PUNCHING: Backporting check_output from 2.7 to 2.6
if "check_output" not in dir(subprocess):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


# Globals
NAME_SERVER = "10.10.10.10"
SUBNET = ["10.1.10.0/24", "10.1.11.0/24"]
VZCTL = "/usr/sbin/vzctl"
VZLIST = "/usr/sbin/vzlist -a"
HOST_NAME = "vlabs.ac.in"
LAB_ID = "engg01"
MAX_VM_ID = 2147483644      # 32-bit; exact value based on trial-and-error
VM_MANAGER_PORT = 8089
VM_MANAGER_DIR = "/root/vm_manager"


class InvalidVMIDException(Exception):
    def __init__(msg):
        Exception.__init__(msg)


def create_VM(VM_ID, VM_spec):
    """ VM_specification is a VMSpec object """
    # Create the VM
    VM_ID = validate_VM_ID(VM_ID)
    (VM_create_args, VM_set_args) = construct_vzctl_args(VM_spec)
    try:
        subprocess.check_call(VZCTL + " create " + VM_ID + VM_create_args, shell=True)
        subprocess.check_call(VZCTL + " start " + VM_ID, shell=True)
        subprocess.check_call(VZCTL + " set " + VM_ID + VM_set_args, shell=True)
    except subprocess.CalledProcessError, e:
        raise e
    return start_VM_manager(VM_ID)

def restart_VM(VM_ID):
    VM_ID = validate_VM_ID(VM_ID)
    # restart VM
    try:
        subprocess.check_call(VZCTL + " restart " + VM_ID, shell=True)
    except subprocess.CalledProcessError, e:
        raise e
    return start_VM_manager(VM_ID)

def start_VM_manager(VM_ID):
    # Copy the VMManager package to the VM
    # Start the VMManager on a chosen port
    # Return the VM's IP and port info
    return (ip_address, VM_MANAGER_PORT)

def stop_VM(VM_ID):
    VM_ID = validate_VM_ID(VM_ID)
    try:
        subprocess.check_call(VZCTL + " stop " + VM_ID, shell=True)
    except subprocess.CalledProcessError, e:
        raise e
    # Return success or failure

def destroy_VM(VM_ID):
    VM_ID = validate_VM_ID(VM_ID)
    try:
        subprocess.check_call(VZCTL + " stop " + VM_ID, shell=True)
        subprocess.check_call(VZCTL + " destroy " + VM_ID, shell=True)
    except subprocess.CalledProcessError, e:
        raise e
    # Return success or failure

def is_running_VM(VM_ID):
    pass

def migrate_VM(VM_ID, destination):
    VM_ID = validate_VM_ID(VM_ID)
    pass

def take_snapshot(VM_ID):
    VM_ID = validate_VM_ID(VM_ID)
    pass

def construct_vzctl_args(VM_spec):
    """ Returns a tuple of vzctl create arguments and set arguments """
    lab_ID = LAB_ID if VM_spec.lab_ID == "" else VM_spec.lab_ID
    host_name = lab_ID + "." + HOST_NAME
    ip_address = find_available_ip()
    os_template = VMUtils.find_os_template(VM_spec.os, VM_spec.os_version)
    (ram, swap) = VMUtils.get_ram_swap(VM_spec.ram, VM_spec.swap)
    (disk_soft, disk_hard) = VMUtils.get_disk_space(VM_spec.diskspace)
    VM_create_args = " --ostemplate " + os_template + \
                     " --ipadd " + ip_address + \
                     " --diskspace " + disk_soft + ":" + disk_hard + \
                     " --hostname " + host_name
    # Note to self: check ram format "0:256M" vs "256M"
    VM_set_args = " --nameserver " + NAME_SERVER + \
                  " --ram " + ram + \
                  " --swap " + swap + \
                  " --save"
    return (VM_create_args, VM_set_args)

def find_available_ip():
    # not designed to be concurrent?
    used_ips = subprocess.check_output(VZLIST, shell=True)
    for subnet in SUBNET:
        ip_network = netaddr.IPNetwork(subnet)
        for ip in list(ip_network):
            if ip == ip_network.network or ip == ip_network.broadcast:
                # e.g. 192.0.2.0 or 192.0.2.255 for subnet 192.0.2.0/24
                continue
            else:
                ip_address = str(ip)
                if ip_address not in used_ips:
                    return ip_address

def validate_VM_ID(VM_ID):
    VM_ID = str(VM_ID).strip()
    m = re.match(r'^([0-9]+)$', VM_ID)
    if m == None:
        raise InvalidVMIDException("Invalid VM ID.  VM ID must be numeric.")
    VM_ID = int(m.group(0))
    if VM_ID <= 100:
        raise InvalidVMIDException("Invalid VM ID.  VM ID must be greater than 100.")
    if VM_ID > MAX_VM_ID:
        raise InvalidVMIDException("Invalid VM ID.  Specify a smaller VM ID.")
    return str(VM_ID)


if __name__ == "__main__":
    # Start an HTTP server and wait for invocation
    # Parse the invocation command and route to 
    # appropriate methods.
    vm_spec = VMSpec.VMSpec()
    create_VM("99100", vm_spec)
    create_VM("99101", vm_spec)
    #create_VM("99102", vm_spec)
    #create_VM("99103", vm_spec)
    destroy_VM("99100")
    destroy_VM("99101")
    #destroy_VM("99102")
    #destroy_VM("99103")

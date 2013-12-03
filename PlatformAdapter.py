# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" An interface for managing VMs for a selected platform. """

# Standard Library imports
import re
import subprocess

# Third party imports
import netaddr

# VLEAD imports
import VMSpec

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
OS = "Ubuntu"
OS_VERSION = "12.04"
RAM = "256M"
SWAP = "512M"



class CentOSVZAdapter:
    """ For CentOS host running OpenVZ virtualization.
        Platform adapter runs on the host machine as "root" user.
    """
    
    def __init__(self):
        pass

    def create_VM(self, VM_ID, VM_spec):
        """ VM_specification is a VMSpec object """
        # Create the VM
        VM_ID = self._validate_VM_ID(VM_ID)
        (VM_create_args, VM_set_args) = self._construct_vzctl_args(VM_spec)
        try:
            subprocess.check_call(VZCTL + " create " + VM_ID + VM_create_args, shell=True)
            subprocess.check_call(VZCTL + " start " + VM_ID, shell=True)
            subprocess.check_call(VZCTL + " set " + VM_ID + VM_set_args, shell=True)
        except subprocess.CalledProcessError, e:
            raise e
        # Start VMManager on the VM
        pass
        # Return VMManager's signature
        #return ("ipaddress", "port")
        pass

    def destroy_VM(self, VM_ID):
        VM_ID = self._validate_VM_ID(VM_ID)
        try:
            subprocess.check_call(VZCTL + " stop " + VM_ID, shell=True)
            subprocess.check_call(VZCTL + " destroy " + VM_ID, shell=True)
        except subprocess.CalledProcessError, e:
            raise e

    def migrate_VM(self, VM_ID, destination):
        VM_ID = self._validate_VM_ID(VM_ID)
        pass

    def take_snapshot(self, VM_ID):
        VM_ID = self._validate_VM_ID(VM_ID)
        pass

    def _construct_vzctl_args(self, VM_spec):
        """ Returns a tuple of vzctl create arguments and set arguments """
        lab_ID = LAB_ID if VM_spec.lab_ID == "" else VM_spec.lab_ID
        host_name = lab_ID + "." + HOST_NAME
        os_template = self._find_os_template(VM_spec.os, VM_spec.os_version)
        ip_address = self._find_available_ip()
        (ram, swap) = self._find_ram_swap(VM_spec.ram, VM_spec.swap)
        (min_diskspace, max_diskspace) = self._find_disk_space(
                                                    VM_spec.min_diskspace,
                                                    VM_spec.max_diskspace)
        VM_create_args = " --ostemplate " + os_template + \
                         " --ipadd " + ip_address + \
                         " --diskspace " + min_diskspace + ":" + max_diskspace + \
                         " --hostname " + host_name
        # Note to self: check ram format "0:256M" vs "256M"
        VM_set_args = " --nameserver " + NAME_SERVER + \
                      " --ram " + ram + \
                      " --swap " + swap + \
                      " --save"
        return (VM_create_args, VM_set_args)

    def _find_available_ip(self):
        # not designed to be concurrent?
        used_ips = subprocess.check_output(VZLIST, shell=True)
        for subnet in SUBNET:
            ip_network = netaddr.IPNetwork(subnet)
            for ip in list(ip_network):
                if ip == ip_network.network or ip == ip_network.broadcast:
                    # Skip if IP is the network IP or broadcast IP
                    # e.g. 192.0.2.0 or 192.0.2.255 for subnet 192.0.2.0/24
                    continue
                else:
                    ip_address = str(ip)
                    if ip_address in used_ips:
                        continue
                    else:
                        return ip_address

    @staticmethod
    def _find_ram_swap(ram, swap):
        
        return ("256M", "512M")

    @staticmethod
    def _find_disk_space(min_diskspace, max_diskspace):
        #min_diskspace = "2G"; max_diskspace = "2.5G"
        return ("2G", "2.5G")

    @staticmethod
    def _find_os_template(os, os_version):
        # What to do when request comes for unavailable OS/version?
        os = OS.upper() if os == "" else os.strip().upper()
        os_version = OS_VERSION if os_version == "" else os_version.strip()
        if os == "UBUNTU":
            if os_version == "12.04" or os_version == "12":
                return "ubuntu-12.04-x86_64"
            elif os_version == "11.10" or os_version == "11":
                return "ubuntu-11.10-x86_64"
        elif os == "CENTOS":
            if os_version == "6.3":
                return "centos-6.3-x86_64"
            elif os_version == "6.2":
                return "centos-6.2-x86_64"
        elif os == "DEBIAN":
            if os_version == "6.0" or os_version == "6":
                return "debian-6.0-x86_64"
        else:
            pass

    @staticmethod
    def _validate_VM_ID(VM_ID):
        VM_ID = str(VM_ID).strip()
        m = re.match(r'^[0-9]+$', VM_ID)
        if m == None:
            print "Invalid VM ID.  VM ID must be numeric."
            return
        else:
            return VM_ID


class CentOSKVMAdapter:
    """ For CentOS host running KVM virtualization """
    def __init__(self):
        pass


class AWSAdapter:
    """ For Amazon Web Services """
    def __init__(self):
        pass


class EucalyptusAdapter:
    """ For Eucalyptus private cloud """
    def __init__(self):
        pass


if __name__ == "__main__":
    # Start an HTTP server and wait for invocation
    # Parse the invocation command and route to 
    # appropriate methods.
    platform_adapter = CentOSVZAdapter()
    vm_spec = VMSpec.VMSpec()
    #platform_adapter.create_VM("99101", vm_spec)
    #platform_adapter.create_VM("99102", vm_spec)
    #platform_adapter.create_VM("99103", vm_spec)
    #platform_adapter.destroy_VM("99100")
    #platform_adapter.destroy_VM("99101")
    #platform_adapter.destroy_VM("99102")
    #platform_adapter.destroy_VM("99103")

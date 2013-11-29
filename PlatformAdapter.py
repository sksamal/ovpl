# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" An interface for managing VMs for a selected platform. """

from re import match
from subprocess import check_call
from subprocess import CalledProcessError

import VMSpec

class CentOSVZAdapter:
    """ For CentOS host running OpenVZ virtualization.
        Platform adapter runs on the host machine as "root" user.
    """
    NAME_SERVER = "10.10.10.10"
    SUBNET = ["10.1.10.0/24", "10.1.11.0/24"]
    VZCTL = "/usr/sbin/vzctl"

    def __init__(self):
        pass

    def create_VM(self, VM_ID, VM_spec):
        """ VM_specification is a VMSpec object """
        # Create the VM
        VM_ID = self._validate_VM_ID(VM_ID)
        (VM_create_args, VM_set_args) = self._construct_vzctl_args(VM_spec)
        try:
            check_call(VZCTL + " create " + VM_ID + VM_create_args, shell=True)
            check_call(VZCTL + " start " + VM_ID, shell=True)
            check_call(VZCTL + " set " + VM_ID + VM_set_args, shell=True)
        except CalledProcessError, e:
            raise e
        # Start VMManager on the VM
        pass
        # Return VMManager's signature
        return ("ipaddress", "port")

    def destroy_VM(self, VM_ID):
        VM_ID = self._validate_VM_ID(VM_ID)
        try:
            check_call(VZCTL + " stop " + VM_ID, shell=True)
            check_call(VZCTL + " destroy " + VM_ID, shell=True)
        except CalledProcessError, e:
            raise e

    def migrate_VM(self, VM_ID, destination):
        VM_ID = self._validate_VM_ID(VM_ID)
        pass

    def take_snapshot(self, VM_ID):
        VM_ID = self._validate_VM_ID(VM_ID)
        pass

    def _construct_vzctl_args(self, VM_spec):
        """ Returns a tuple of vzctl create arguments and set arguments """
        VM_args = ""
        # Setting VM defaults
        ram = "256M"
        swap = "512M"
        lab_ID = "engg01"
        os = "Ubuntu"
        os_version = "12.04"
        min_diskspace = "2G"
        max_diskspace = "2.5G"
        ip_address = "10.10.10.10"
        name_server = "10.10.10.10"
        # Form vzctl create arguments
        pass
        # Form vzctl set arguments
        pass
        # Return the tuple
        pass

    @staticmethod
    def _validate_VM_ID(self, VM_ID):
        VM_ID = str(VM_ID).strip()
        # Check for numeric values
        m = re.match(r'^[0-9]+$', VM_ID)
        if m == None:
            print "Invalid VM ID.  VM ID must be numeric."
            return
        else:
            return VM_ID


class CentOSKVMPAdapter:
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
    # Start a web server and wait for invocation
    # Parse the invocation command and route to 
    # appropriate methods.
    platform_adapter = CentOSVZAdapter()
    platform_adapter.destroy_VM("99100")
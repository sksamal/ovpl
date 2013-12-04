# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" VMPool module description """

__all__ = [
    'VMProxy',
    'VMPool',
    ]

import VMSpec

class VMProxy:
    """ The proxy object corresponding to a VM """

    def __init__(self, VM_ID, ip_address, port):
        self.VM_ID = VM_ID.strip()
        self.ip_address = ip_address.strip()
        self.port = port.strip()


class VMPool:
    """ Manages a pool of VMs or VMProxy's """

    def __init__(self, adapter_ip, adapter_port):
        self.VMs = []
        self.adapter_ip = adapter_ip
        self.adapter_port = adapter_port

    def create_VM(self, VM_spec):
        # Allocate a VM_ID
        # Invoke platform adapter
        # Construct VMProxy
        # Add to VMs list
        pass

    def destroy_VM(self, VM_ID):
        # Invoke platform adapter
        # Delete entry from VMs list
        pass

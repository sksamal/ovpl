# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" Representation of a VM specification. """

class VMSpec:
    """ Represents build and installation specifications of a VM. """
    def __init__(self):
        # Temporarily setting defaults
        self.lab_ID = "test99"
        self.os = "Ubuntu"
        self.os_version = "12.04"
        self.ram = "256M"
        self.swap = "512M"
        self.min_diskspace = "2G"
        self.max_diskspace = "2.5G"
        self.ip_address = "10.10.10.10"
        self.name_server = "10.10.10.10"
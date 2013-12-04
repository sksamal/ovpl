# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" Representation of a VM specification. """

class VMSpec:
    """ Represents build and installation specifications of a VM. """
    def __init__(self, specs):
        # Temporarily setting defaults
        self.lab_ID = specs['lab_ID'] #"test99"
        self.os = specs['os'] #"Ubuntu"
        self.os_version = specs['os_version'] #"12.04"
        self.ram = specs['ram'] #"256M"
        self.swap = specs['swap'] #"512M"
        self.diskspace = specs['diskspace'] #"2G"

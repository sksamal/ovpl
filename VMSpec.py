# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" Representation of a VM specification. """

class VMSpec:
    """ Represents build and installation specifications of a VM. """
    def __init__(self, specs):
        # Temporarily setting defaults
        self.lab_ID = specs['lab_ID'][0] #"test99"
        self.os = specs['os'][0] #"Ubuntu"
        self.os_version = specs['os_version'][0] #"12.04"
        self.ram = specs['ram'][0] #"256M"
        self.swap = specs['swap'][0] #"512M"
        self.diskspace = specs['diskspace'][0] #"2G"

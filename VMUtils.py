# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" Utilities for use in OVPL application. """

__all__ = [
    'get_ram_swap',
    'get_disk_space',
    'convert_to_megs',
    'find_os_template',
    ]

import re

OS = "Ubuntu"
OS_VERSION = "12.04"
RAM = "256M"
RAM_MAX = "2048M"
SWAP = "512M"
SWAP_MAX = "4096M"
DISK_SOFT = "2G"
DISK_SOFT_MAX = "200G"
DISK_HARD_MUL = 1.5


def get_ram_swap(ram, swap):
    ram = convert_to_megs(ram)
    if ram == 0: 
        ram = convert_to_megs(RAM)
    elif ram > convert_to_megs(RAM_MAX): 
        ram = convert_to_megs(RAM_MAX) 
    ram = str(ram) + "M"
    swap = convert_to_megs(swap)
    if swap == 0: 
        swap = convert_to_megs(SWAP) 
    elif swap > convert_to_megs(SWAP_MAX): 
        swap = convert_to_megs(SWAP_MAX)
    swap = str(swap) + "M"
    return (ram, swap)

def get_disk_space(disk_soft):
    disk_soft = convert_to_megs(disk_soft)
    if disk_soft == 0: 
        disk_soft = convert_to_megs(DISK_SOFT)
    elif disk_soft > convert_to_megs(DISK_SOFT_MAX): 
        disk_soft = convert_to_megs(DISK_SOFT_MAX)
    disk_soft = int(disk_soft / 1024)       # Converting to Gigs
    disk_hard = disk_soft * DISK_HARD_MUL
    disk_soft = str(disk_soft) + "G"
    disk_hard = str(disk_hard) + "G"
    return (disk_soft, disk_hard)

def convert_to_megs(value):
    m = re.match(r'([0-9]+)\s*([a-zA-Z]+)', value)
    if m == None:
        return 0
    quantity = int(m.group(1))
    unit = m.group(2)
    if "G" in unit.upper():     # Gigabytes
        quantity = quantity * 1024
    elif "K" in unit.upper():   # Kilobytes
        quantity = int(quantity / 1024)
    elif "M" in unit.upper():   # Megabytes
        pass
    else:                       # Invalid unit?
        # Work on this later
        print "Invalid unit"
        return 0
    return quantity

def find_os_template(os, os_version):
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


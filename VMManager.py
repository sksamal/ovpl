# Author: Chandan Gupta
# Contact: chandan@vlabs.ac.in

""" An interface for managing VMs for a selected platform. """

import subprocess

# Run this command for me, please.
# how long has your VM been running?
# what is your memory footprint?
# what is your diskspace footprint?
# what processes are currently running?
# what is your CPU load?
# 


def execute(command):
    # do some validation
    subprocess.check_call(command, shell=True)




if __name__ == "__main__":
    execute("ls -l")


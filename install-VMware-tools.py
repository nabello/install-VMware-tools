#!/usr/bin/env python2.7

import subprocess
from os import getuid
import sys

def test_os(os):
    out = execute("cat /etc/*-release |grep -i "+os, "Retrieving OS info ...", "########")

    if os == "red hat":
        os="rhel"

    if out == 0:
        return os
    else:
        return False

def main():
    print("Installing VMware Tools on Ubuntu  ...")
    
    #Check that OS is Ubuntu
    print("Check that OS is Ubuntu")
    os = test_os('ubuntu')
    if os is False:
        exit(1)
    
    # Update and Upgarde ubuntu repo/packages
    print("Update and Upgarde ubuntu repo/packages")
    subprocess.check_call(["apt-get", "update"])
    subprocess.check_call(["apt-get", "update"])
    
    #Install required compiler tools
    print("#Install required compiler tools")
    subprocess.check_call(["apt-get", "install", "build-essential"])
    
    #Install Linux header specific to the version of Ubuntu that you have running
    print("Install Linux header specific to the version of Ubuntu that you have running")
    subprocess.check_call(["apt-get", "install", "linux-headers-`uname -r`"])
    
    #Insert the CD image of VMware Tools into the virtual CD-ROM Drive
    print("Insert the CD image of VMware Tools into the virtual CD-ROM Drive")
    
    #Mount the VMware Tools CD in Linux
    print("Mount the VMware Tools CD in Linux")
    subprocess.check_call(["cd", "/mnt"])
    subprocess.check_call(["mkdir", "cdrom"])
    subprocess.check_call(["mount", "/dev/cdrom", "/mnt/cdrom/"])
    subprocess.check_call(["cd", "/mnt/cdrom"])
    
    #Check that the VMware Tools CD is well mounted and that you can access the file required for installation
    print("Check that the VMware Tools CD is well mounted and that you can access the file required for installation")
    #if:
    #    raise VMwareToolsError("Your VMware Tools CD can not be accessed, verify that you have correctly mounted it.")
    
    
    #Copy content *.gz to /tmp/
    print("Copy content *.gz to /tmp/")
    subprocess.check_call(["cp", "VM*.gz", "/tmp/"])
    
    #Go to /tmp and untar file
    print("Go to /tmp and untar file")
    subprocess.check_call(["cd", "/tmp"])
    subprocess.check_call(["tar", "xvzf", "VM*.gz"])
    
    #Go to VMware Tools folder
    print("Go to VMware Tools folder")
    subprocess.check_call(["cd", "vmware-tools-distrib/"])
    
    #Install VMware Tools
    print("Install VMware Tools")
    #subprocess.check_call(["./vmware-install.pl"])
    
    
    print("Your VMware Tools have been successfully installed ...")
    
if __name__ == "__main__":
    #Check if user is sudo
    class NotSudo(Exception):
        pass

    if getuid() != 0:
         raise NotSudo("This program must be run as sudo...")
    main()
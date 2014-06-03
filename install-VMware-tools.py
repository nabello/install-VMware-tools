#!/usr/bin/env python2.7

import subprocess
import os
import sys


def createBnr(msg,position):
    msgSize = len(msg)
    width = 60
    heigth = 3
    topBottom = ''
    middle = ''

    if msgSize >= width:
        width += 30

    halfMsgSize = msgSize / 2
    halfWidth = width/2
    indexStartMsg = halfWidth - halfMsgSize

    for i in range(1,(width-msgSize)) :

        if i == 1 or i == (width-msgSize-1):
            topBottom += '*'
            middle += '*'
        elif i == indexStartMsg:
            for j in range(0,msgSize):
                topBottom += '*'
                middle = middle+msg[j]
        else:
            topBottom += '*'
            middle += ' '

    if position == 'top':
        return '\n\n\n'+topBottom+'\n'+middle+'\n'+topBottom+'\n'
    elif position == 'bottom':
        return '\n'+topBottom+'\n'+middle+'\n'+topBottom+'\n\n\n'

    return '\n'+topBottom+'\n'+middle+'\n'+topBottom+'\n'


def execute(cmd,msg1,msg2):
    print(createBnr(msg1,"top"))
    rsp = subprocess.call(cmd, shell=True)
    print(createBnr(msg2,"bottom"))
    return rsp


def test_os(os_type):
    out = execute("cat /etc/*-release |grep -i "+os_type, "Check that OS is Ubuntu", "########")

    if os_type == "red hat":
        os_type = "rhel"

    if out == 0:
        return os_type
    else:
        return False


def main():
    print("Installing VMware Tools on Ubuntu  ...")
    
    #Check that OS is Ubuntu
    os_type = test_os('ubuntu')
    if os_type is False:
        exit(1)
    
    # Update and Upgarde ubuntu repo/packages
    execute("apt-get update", "Update and Upgarde ubuntu repo/packages","")
    execute("apt-get update", "", "########")
    
    #Install required compiler tools
    execute("apt-get -y install build-essential", "Install required compiler tools", "########")
    
    #Install Linux header specific to the version of Ubuntu that you have running
    execute("apt-get -y install linux-headers-`uname -r`", "Install Linux header", "########")
    
    #Insert the CD image of VMware Tools into the virtual CD-ROM Drive
    print("Insert the CD image of VMware Tools into the virtual CD-ROM Drive")
    
    #Mount the VMware Tools CD in Linux
    os.chdir("/mnt")
    execute("mkdir cdrom", "Mount the VMware Tools CD in Linux", "")
    
    execute("mount /dev/cdrom /mnt/cdrom/", "", "########")
    if os.path.ismount("/mnt/cdrom/") == False:
        raise NameError ("The mount failed verify in VM -> Guest -> Install/Upgrade VMware Tools")
    
    os.chdir("/mnt/cdrom")
    
    #Copy content *.gz to /tmp/
    execute("cp VM*.gz /tmp/", "Copy content *.gz to /tmp/", "########")
        
    #Check that the VMware Tools CD is well mounted and that you can access the file required for installation
    print("Check that the VMware Tools CD is well mounted and that you can access the file required for installation")
    if os.path.exists("/tmp/VM*.gz"):
        raise NameError("Your VMware Tools CD can not be accessed, verify that you have correctly mounted it.")
    
    #Go to /tmp and untar file
    os.chdir("/tmp")
    execute("tar xvzf VM*.gz", "Go to /tmp and untar file", "########")
    
    #Go to VMware Tools folder
    print("Go to VMware Tools folder")
    os.chdir("vmware-tools-distrib/")
    
    #Install VMware Tools
    print("Install VMware Tools")
    execute("./vmware-install.pl", "Install VMware Tools", "########")
    
    #Clean /tmp folder of VMwareTools install scripts files
    os.chdir("/tmp")
    execute("rm VM*.gz", "Clean /tmp folder of VMwareTools install scripts files", "########")
    
    
    print("Your VMware Tools have been successfully installed ...")
    
if __name__ == "__main__":
    #Check if user is sudo
    class NotSudo(Exception):
        pass

    if os.getuid() != 0:
         raise NotSudo("This program must be run as sudo...")
    main()
import libvirt
import sys
import logging


def get_connection_readonly():
    try:
        conn = libvirt.openReadOnly("qemu:///system")
    except libvirt.libvirtError:
        logging.fatal("Failed to open connection to the hypervisor")
        sys.exit(1)

    return conn

def get_connection():
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError:
        logging.fatal("Failed to open connection to the hypervisor")
        sys.exit(1)

    return conn

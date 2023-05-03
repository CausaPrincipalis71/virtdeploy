import libvirt
import sys


def get_connection_readonly():
    try:
        conn = libvirt.openReadOnly("qemu:///system")
    except libvirt.libvirtError:
        print('Failed to open connection to the hypervisor')
        sys.exit(1)

    return conn

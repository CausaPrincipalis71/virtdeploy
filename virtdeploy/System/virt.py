import libvirt
import sys
import logging


try:
    connReadOnly = libvirt.openReadOnly("qemu:///system")
except libvirt.libvirtError:
    logging.fatal("Failed to open connection to the hypervisor")
    sys.exit(1)

try:
    conn = libvirt.open("qemu:///system")
except libvirt.libvirtError:
    logging.fatal("Failed to open connection to the hypervisor")
    sys.exit(1)

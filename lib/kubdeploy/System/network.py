import re
from lib.kubdeploy.System.virt import get_connection_readonly

def get_existing_connections_names():
    conn = get_connection_readonly()
    return [x.name() for x in conn.listAllNetworks()]

def get_existing_connections_ifaces():
    conn = get_connection_readonly()
    return [x.bridgeName() for x in conn.listAllNetworks()]

def get_existing_connections_ifaces_nums():
   ifaces = get_existing_connections_ifaces()
   return [int(''.join(filter(str.isdigit, iface))) for iface in ifaces]

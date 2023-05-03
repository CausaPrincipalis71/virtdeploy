import uuid

from virtdeploy.System.virt import get_connection_readonly
from virtdeploy.System.virt import get_connection
from virtdeploy.Utils.networking import vid_provided

#Getters section
def get_existing_connections_names():
    conn = get_connection_readonly()
    return [x.name() for x in conn.listAllNetworks()]

def get_existing_connections_ifaces():
    conn = get_connection_readonly()
    return [x.bridgeName() for x in conn.listAllNetworks()]

def get_existing_connections_ifaces_nums():
   ifaces = get_existing_connections_ifaces()
   return [int(''.join(filter(str.isdigit, iface))) for iface in ifaces]

#Working with networks
def create_network(name, subnet, ifaceNum):
    conn = get_connection()
    generated_uuid = uuid.uuid4()
    mac = vid_provided("52:54:00")
    xml = f"""
    <network>
      <name>{name}</name>
      <uuid>{generated_uuid}</uuid>
      <forward mode='nat'>
        <nat>
          <port start='1024' end='65535'/>
        </nat>
      </forward>
      <bridge name='virbr{ifaceNum}' stp='on' delay='0'/>
      <mac address='{mac}'/>
      <domain name='{name}'/>
      <ip address='192.168.{subnet}.1' netmask='255.255.255.0'>
        <dhcp>
          <range start='192.168.{subnet}.128' end='192.168.{subnet}.254'/>
        </dhcp>
      </ip>
    </network>"""

    net = conn.networkDefineXML(xml)
    try:
        net.create()
    except libvirt.libvirtError as e:
        #print(repr(e), file=sys.stderr)
        print("error")
        net.undefine()
        conn.close()
        exit(1)

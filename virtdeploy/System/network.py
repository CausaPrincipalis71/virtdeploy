import uuid
import xml.etree.cElementTree as ET
import logging
import libvirt

import virtdeploy.Utils.genmac as genmac

from virtdeploy.System.virt import conn, connReadOnly


# Getters section
def get_existing_connections_names():
    return [x.name() for x in connReadOnly.listAllNetworks()]


def get_existing_connections_ifaces():
    return [x.bridgeName() for x in connReadOnly.listAllNetworks()]


def get_existing_connections_ifaces_nums():
    ifaces = get_existing_connections_ifaces()
    return [int(''.join(filter(str.isdigit, iface))) for iface in ifaces]


def get_busy_subnets():
    list = [0, 1]
    for x in connReadOnly.listAllNetworks():
        xml = ET.fromstring(x.XMLDesc())
        ip = xml.find("ip").get("address").split('.')
        if (ip[0] == '192'):
            list.append(int(ip[2]))
    return list


def getNetworkUuid(netName):
    for net in connReadOnly.listAllNetworks():
        if net.name == netName:
            return net.UUIDString


def getNetworkBridge(netName):
    for net in connReadOnly.listAllNetworks():
        if net.name == netName:
            return net.bridgeName


# Working with networks
def create_network(name, subnet, ifaceNum):
    generated_uuid = uuid.uuid4()
    mac = genmac.vid_provided("52:54:00")
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
        net.setAutostart(True)
        return net
    except libvirt.libvirtError as e:
        logging.fatal(repr(e))
        net.undefine()
        conn.close()
        exit(1)

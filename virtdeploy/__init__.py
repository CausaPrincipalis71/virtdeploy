import os

from virtdeploy.System.virt import conn

import virtdeploy.Utils.random as rand
import virtdeploy.System.network as network
import virtdeploy.System.cluster as cluster

VERSION = "1.0.0"

_prefix = os.path.join(os.path.dirname(__file__))
_dataPrefix = os.path.join(os.path.dirname(__file__))


def createNet(name):
    subnet = rand.genRandomInRangeWithout(0, 255, network.get_busy_subnets())
    ifacenum = max(network.get_existing_connections_ifaces_nums()) + 1

    return network.create_network(name, subnet, ifacenum)


def destroyCluster(name):
    net = conn.networkLookupByName(name)
    net.destroy()
    net.undefine()
    cluster.removeClusterDir(name)


def initCluster(tomlFile):
    name = cluster.getClusterName(tomlFile)

    net = createNet(name)
    if net is None:
        return None

    try:
        cluster.createClusterDir(name, tomlFile, net.XMLDesc())
        cluster.createSshKey(name)
        cluster.downloadClusterImage(name, tomlFile)
        cluster.createDomains(name, tomlFile)
    except Exception as e:
        destroyCluster(name)
        print(e.with_traceback())

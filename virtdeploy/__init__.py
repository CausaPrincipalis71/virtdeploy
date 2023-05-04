import os

import virtdeploy.Utils.random as rand

import virtdeploy.System.network as net

VERSION = "1.0.0"
_prefix = os.path.join(os.path.dirname(__file__))


def createNet(name):
    subnet = rand.genRandomInRangeWithout(0, 255, net.get_busy_subnets())
    ifacenum = max(net.get_existing_connections_ifaces_nums()) + 1

    return net.create_network(name, subnet, ifacenum)

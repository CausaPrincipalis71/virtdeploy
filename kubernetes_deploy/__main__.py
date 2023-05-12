import argparse
import sys
import kubernetes_deploy


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', metavar="ClusterName",  help="Install kubernetes on ClusterName")

    return parser


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])


if namespace.run:
    kubernetes_deploy.createVariablesFile(namespace.run)
    kubernetes_deploy.installEtcd(namespace.run)
    sys.exit(0)

import os
import tomlkit
import uuid
import subprocess
import shutil
import pathlib


home = os.path.expanduser("~")
_prefix = os.path.join(os.path.dirname(__file__))


def createVariablesFile(clusterName):
    deployDir = f"{home}/.kubernetes_deploy/{clusterName}"
    clusterDir = f"{home}/.virtdeploy/{clusterName}"
    os.makedirs(deployDir)
    varFile = open(f"{deployDir}/vars.sh", "w")
    varFile.write("#!/bin/bash\n")

    etcdToken = uuid.uuid4()

    for domainName in os.listdir(f"{clusterDir}/domains"):
        ip = tomlkit.parse(open(f"{clusterDir}/domains/{domainName}/info.toml", "r").read()).get("Network").get("ip")
        varFile.write(f"{domainName}_IP={ip}\n{domainName}_Hostname={domainName}\n\n")

    varFile.write("thisHostname=$(hostname)\nthisIp=$(hostname -i)\n\n")
    varFile.write(f"etcdToken={etcdToken}\npodSubnet=10.244.0.0/16\nserviceSubnet=10.46.0.0/16\n")
    varFile.close()

    shutil.copytree(f"{_prefix}/ansible_playbooks", f"{deployDir}/ansible_playbooks")
    shutil.copytree(f"{_prefix}/scripts", f"{deployDir}/scripts")

    subprocess.run(["ansible-playbook", "-i", f"{clusterDir}/ansible_hosts", f"{deployDir}/ansible_playbooks/copy-file.yml", "--extra-var", f"DIR={deployDir} NAME=vars.sh"])


def installEtcd(clusterName):
    clusterDir = f"{home}/.virtdeploy/{clusterName}"
    deployDir = f"{home}/.kubernetes_deploy/{clusterName}"

    etcdClusterInfo = ""

    for etcdDomain in pathlib.Path(f"{clusterDir}/domains").glob("etcd*"):
        etcdClusterInfo += f"${{{etcdDomain.name}_Hostname}}=http://${{{etcdDomain.name}_IP}}:2380,"

    with open(f"{deployDir}/scripts/setupEtcd.sh") as f:
        oldData = f.read()
    newData = oldData.replace("{CLUSTER_REPLACE}", f"{etcdClusterInfo[:-1]}")
    with open(f"{deployDir}/scripts/setupEtcd.sh", "w") as f:
        f.write(newData)

    return subprocess.run(["ansible-playbook", "-i", f"{clusterDir}/ansible_hosts", f"{deployDir}/ansible_playbooks/install-etcd.yml", "--extra-var", f"DIR={deployDir} ETCD_SCRIPT_FILE=setupEtcd.sh"])

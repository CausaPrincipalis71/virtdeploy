import os
import shutil
import wget

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization
from virtdeploy.System.virt import conn

import virtdeploy.Utils.toml as toml
import virtdeploy.System.image as image
import virtdeploy.System.domain as domain


home = os.path.expanduser("~")


def createSshKey(name):
    key = rsa.generate_private_key(key_size=2048, public_exponent=65537)
    private_key = key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH)

    with open(f"{home}/.virtdeploy/{name}/keys/key.private", "w") as privateFile:
        privateFile.write(private_key.decode("utf-8"))
        os.chmod(f"{home}/.virtdeploy/{name}/keys/key.private", 0o600)

    with open(f"{home}/.virtdeploy/{name}/keys/key.public", "w") as publicFile:
        publicFile.write(public_key.decode("utf-8"))


def createClusterDir(name, tomlFile, netinfo):
    os.makedirs(f"{home}/.virtdeploy/{name}")
    os.mkdir(f"{home}/.virtdeploy/{name}/images")
    os.mkdir(f"{home}/.virtdeploy/{name}/configs")
    os.mkdir(f"{home}/.virtdeploy/{name}/domains")
    os.mkdir(f"{home}/.virtdeploy/{name}/keys")

    with open(f"{home}/.virtdeploy/{name}/configs/net", "w") as f:
        f.write(netinfo)

    shutil.copy2(tomlFile, f"{home}/.virtdeploy/{name}/configs/desc")


def removeClusterDir(name):
    for domainName in os.listdir(f"{home}/.virtdeploy/{name}/domains"):
        domain = conn.lookupByName(f"{name}-{domainName}")
        domain.destroy()
        domain.undefine()
    shutil.rmtree(f"{home}/.virtdeploy/{name}")


def downloadClusterImage(name, tomlFile):
    osImage = getClusterImage(tomlFile)
    link = image.getImageLink(osImage)
    filename = image.getImageFilename(osImage)

    if link is None:
        return None
    print(f"Downloading {filename} to {home}/.virtdeploy/{name}/images/...")
    return wget.download(link, f"{home}/.virtdeploy/{name}/images/{filename}")


def createDomains(name, tomlFile):
    imageFile = getImageFile(name, tomlFile)
    imageFilename = imageFile.split('/')[-1]
    domains = toml.getData(tomlFile).get("Cluster").get("domain")
    with open(f"{home}/.virtdeploy/{name}/keys/key.public", 'r') as sshKeyFile:
        sshKey = sshKeyFile.read()
    machineIpNum = 2

    for domainType in domains:
        for i in range(domains.get(domainType).get("amount")):
            # Deploying a domain
            domainDir = f"{home}/.virtdeploy/{name}/domains/{domainType}{i}"
            os.mkdir(domainDir)
            # Copying image
            shutil.copy(imageFile, domainDir)
            # Creating initImage
            domain.createBaseMetaData(f"{domainType}{i}", f"{domainDir}/meta-data.yaml")
            domain.createBaseUserData(sshKey, f"{domainDir}/user-data.yaml")
            domain.createInitImage(domainDir)
            # Creating domain
            domain.createDomain(domainDir, [domainType], i, name, machineIpNum, imageFilename)
            machineIpNum += 1


def getImageFile(name, tomlFile):
    osImage = getClusterImage(tomlFile)
    filename = image.getImageFilename(osImage)

    return f"{home}/.virtdeploy/{name}/images/{filename}"


def getClusterName(tomlDesk):
    return toml.getData(tomlDesk).get("Cluster").get("name")


def getClusterImage(tomlDesk):
    return toml.getData(tomlDesk).get("Cluster").get("image")

import os
import shutil
import wget

import virtdeploy.Utils.toml as toml
import virtdeploy.System.image as image
import virtdeploy.System.domain as domain


home = os.path.expanduser("~")


def createClusterDir(name, tomlFile, netinfo):
    os.makedirs(f"{home}/.virtdeploy/{name}")
    os.mkdir(f"{home}/.virtdeploy/{name}/images")
    os.mkdir(f"{home}/.virtdeploy/{name}/configs")
    os.mkdir(f"{home}/.virtdeploy/{name}/domains")

    with open(f"{home}/.virtdeploy/{name}/configs/net", "w") as f:
        f.write(netinfo)

    shutil.copy2(tomlFile, f"{home}/.virtdeploy/{name}/configs/desc")


def removeClusterDir(name):
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
    sshKey = toml.getData(tomlFile).get("UserData").get("sshKey")

    for domainType in domains:
        for i in range(domains.get(domainType).get("amount")):
            # Deploying a domain
            domainDir = f"{home}/.virtdeploy/{name}/domains/{domainType}-{i}"
            os.mkdir(domainDir)
            # Copying image
            shutil.copy(imageFile, domainDir)
            # Creating initImage
            domain.createBaseMetaData(f"{domainType}-{i}", f"{domainDir}/meta-data.yaml")
            domain.createBaseUserData(sshKey, f"{domainDir}/user-data.yaml")
            domain.createInitImage(domainDir)
            # Creating domain
            domain.createDomain(domainDir, [domainType], i, name, imageFilename)


def getImageFile(name, tomlFile):
    osImage = getClusterImage(tomlFile)
    filename = image.getImageFilename(osImage)

    return f"{home}/.virtdeploy/{name}/images/{filename}"


def getClusterName(tomlDesk):
    return toml.getData(tomlDesk).get("Cluster").get("name")


def getClusterImage(tomlDesk):
    return toml.getData(tomlDesk).get("Cluster").get("image")

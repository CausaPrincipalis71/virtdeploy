import os
import shutil
import wget

import virtdeploy.Utils.toml as toml
import virtdeploy.System.image as image


def createClusterDir(name, tomlFile, netinfo):
    home = os.path.expanduser("~")
    os.makedirs(f"{home}/.virtdeploy/{name}")
    os.mkdir(f"{home}/.virtdeploy/{name}/images")
    os.mkdir(f"{home}/.virtdeploy/{name}/configs")
    os.mkdir(f"{home}/.virtdeploy/{name}/domains")

    with open(f"{home}/.virtdeploy/{name}/configs/net", "w") as f:
        f.write(netinfo)

    shutil.copy2(tomlFile, f"{home}/.virtdeploy/{name}/configs/desc")


def downloadClusterImage(name, tomlFile):
    home = os.path.expanduser("~")
    osImage = getClusterImage(tomlFile)
    link = image.getImageLink(osImage)
    filename = image.getImageFilename(osImage)

    if link is None:
        return None
    print(f"Downloading {filename} to {home}/.virtdeploy/{name}/images/...")
    return wget.download(link, f"{home}/.virtdeploy/{name}/images/{filename}")


def getImageFile(name, tomlFile):
    home = os.path.expanduser("~")
    osImage = getClusterImage(tomlFile)
    filename = image.getImageFilename(osImage)

    return f"{home}/.virtdeploy/{name}/images/{filename}"

def getClusterName(tomlDesk):
    return toml.getData(tomlDesk).get("Cluster").get("name")


def getClusterImage(tomlDesk):
    return toml.getData(tomlDesk).get("Cluster").get("image")

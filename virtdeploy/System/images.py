import virtdeploy
import logging


import virtdeploy.Utils.toml as toml


def getImagesData():
    data = toml.get_data(virtdeploy._prefix + "/data/images.toml")
    if data is None:
        logging.fatal(f"Cannot find {virtdeploy._prefix}/data/images.toml, please create it manually")
        exit(1)

    return data


def isImageExist(name):
    data = getImagesData()
    return data.get(name) is not None


def getImageLink(name):
    data = getImagesData()

    if isImageExist(name) is False or data.get(name).get("link") is None:
        logging.warn(f"Cannot find info about {name}, please add it manually in {virtdeploy._prefix}/data/images.toml")
        return None

    return data.get(name).get("link")


def addNewImage(name, link):
    data = {name: {"link": link}}

    if isImageExist(name) is True:
        logging.warn(f"Cannot add {name} in {virtdeploy._prefix}/data/images.toml. It`s already exists")
        return False

    return toml.write_to(virtdeploy._prefix + "/data/images.toml", data)

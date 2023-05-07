import tomlkit
import logging


def getData(fname):
    try:
        with open(fname, "rb") as f:
            data = tomlkit.load(f)
    except IOError as e:
        logging.warn(repr(e))
        return None
    return data


def writeTo(fname, data):
    try:
        with open(fname, "a") as f:
            f.write("\n" + tomlkit.dumps(data))
    except IOError as e:
        logging.warn(repr(e))
        return False

import tomlkit
import os.path
import logging

def get_data(fname):
    try:
        with open(fname, "rb") as f:
            data = tomlkit.load(f)
    except IOError as e:
        logging.warn(repr(e))
        return None
    return data

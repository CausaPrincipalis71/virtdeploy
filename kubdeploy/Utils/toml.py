import tomlkit

def get_data(fname):
    with open(fname, "rb") as f:
        data = tomlkit.load(f)

    return data

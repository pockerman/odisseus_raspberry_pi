

def read_config(filename):

    """
        Read the json configuration file and
        return a map with the config entries
    """
    with open(filename) as json_file:
        configuration = json.load(json_file)
        return configuration

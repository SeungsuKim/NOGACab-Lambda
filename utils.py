import yaml


# A dictionary object which value can be access with dot notation.
class ObjDict(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError("No such key: " + key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError("No such key: " + key)


# Returns a ObjDict object containing certificate.
def load_yaml_config(filename):
    print("Start loading {}".format(filename))
    with open(filename, 'r') as stream:
        print("Loaded {}".format(filename))
        return ObjDict(yaml.load(stream))

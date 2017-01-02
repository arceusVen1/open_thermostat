from open_ds18b20.fichier import ProbeConfigFile
from os import rename, path


class PlugConfigFile(ProbeConfigFile):
    """deals with th config file of the plug
    """

    def __init__(self, path):
        super(PlugConfigFile, self).__init__(path)

    def rename(self, name):
        self.closeFile()
        parent_path = path.dirname(self.path)
        rename(parent_path + "/" + name, self.path)
        self.path = parent_path + "/" + name
        self.file = open(self.path, 'r')

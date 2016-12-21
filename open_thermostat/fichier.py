from open_ds18b20.fichier import ProbeConfigFile
from os import rename, path


class PlugConfigFile(ProbeConfigFile):
    """deals with th config file of the plug
    """

    def __init__(self, path):
        super(PlugConfigFile, self).__init__(path)

    def edit(self):
        super(PlugConfigFile, self).edit()

    def exists(self):
        super(PlugConfigFile, self).exists()

    def create(self):
        super(PlugConfigFile, self).create()

    def register(self):
        super(PlugConfigFile, self).register()

    def __save(self):
        super(PlugConfigFile, self).__save()

    def readData(self):
        super(PlugConfigFile, self).readData()

    def rename(self, name):
        self.closefile()
        parent_path = path.dirname(self.path)
        rename(parent_path + name, self.path)
        self.path = parent_path + name
        self.file = open(self.path, 'r')

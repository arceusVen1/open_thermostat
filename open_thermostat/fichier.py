from open_ds18b20.fichier import ProbeConfigFile


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

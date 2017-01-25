from open_ds18b20.fichier import ProbeConfigFile


class PlugConfigFile(ProbeConfigFile):
    """deals with th config file of the plug
    """

    def __init__(self, path):
        super(PlugConfigFile, self).__init__(path)
        if self.exists():
            self.edit()

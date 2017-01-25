"""
TODO: plug_config.json -> {light:[{id:, slug:, start:, end:, state:}], thermostat:[{}], hygro:[{}]}
    - find a solutin to add the new parameters
"""


from fichier import PlugConfigFile
from gpiozero import Energenie
PATH = "/home/pi/ds18b20_conf/plugs/plug_config.json"


def _is_int(number):
    """check if the type is a int or not

    Args:
        number (obj): the number you want to test

    Returns:
        bool: True if number is a int
    """
    return isinstance(number, int)


def _is_string(string):
    """check if the type is a string or not

    Args:
        string (obj): the string you want to check

    Returns:
        bool: True if string is really a string
    """
    return isinstance(string, str)


class Materials:
    """represents the plugs or relay board
    """

    def __init__(self):
        path = PATH
        self.config = PlugConfigFile(path)
        self.settings = {"lighting": [], "thermostat": [], "hygrostat": []}

    def has_config(self):
        """test if the config file exist and has been filled

        Returns:
            bool: true if the config exists, false otherwise
        """
        if not self.config.exists() or (hasattr(self.config, "nbline") and
                                        self.config.nbline == 0):
            return False
        else:
            self.allow_config()
            return True

    def allow_config(self):
        """create the file if needed and open it
        """
        self.config.create()
        self.config.edit()

    def get_data(self):
        """load the data and change the settings to match the data

        Returns:
            dict: the new settings
        """
        self.config.get_data()
        self.settings = self.config.settings
        return self.settings

    def set_data(self):
        """registers the settings in the config and rename the file properly
        """
        self.config.settings = self.settings
        self.config.register()

    def add_plug(self, plug):
        """
        To add the plug in the settings of the config or overwrite an existing one (not DRY yet)

        :param plug: a plug whom to config is to add
        :type plug: Plug
        """
        if not isinstance(plug, Plug):
            raise TypeError("no correct plug given")
        id_ = plug.get_id()
        therms = self.get_thermoplugs()
        lights = self.get_lightplugs()
        hygros = self.get_hygroplugs()
        if id_ == 0:
            plug.set_id(len(therms) + len(lights) + len(hygros))
            if isinstance(plug, ThermoPlug):
                therms.append(plug.settings)
            if isinstance(plug, LightPlug):
                lights.append(plug.settings)
            if isinstance(plug, HygroPlug):
                hygros.append(plug.settings)
        else:
            flag = False
            if isinstance(plug, ThermoPlug):
                for i in range(len(therms)):
                    if therms[i]["id"] == id_:
                        therms[i] = plug.settings
                        print("Plug settings registered as a thermostat plug\n")
                        flag = True
                        break
            elif isinstance(plug, LightPlug):
                for i in range(len(lights)):
                    if lights[i]["id"] == id_:
                        lights[i] = plug.settings
                        print("Plug settings registered as a lighting plug\n")
                        flag = True
                        break
            elif isinstance(plug, HygroPlug):
                for i in range(len(hygros)):
                    if hygros[i]["id"] == id_:
                        hygros[i] = plug.settings
                        print("Plug settings registered as a hygrostat plug\n")
                        flag = True
                        break
            if not flag:
                raise ValueError("the id of the probe does not match any existing")

    def get_thermoplugs(self):
        return self.settings["thermostat"]

    def get_lightplugs(self):
        return self.settings["lighting"]

    def get_hygroplugs(self):
        return self.settings["hygrostat"]


class Plug:
    """deals with the electric plug Energenie and relay
    """

    def __init__(self, settings):
        self.settings = settings

    def get_id(self):
        return self.settings["id"]

    def set_id(self, id_):
        """
        Sets the unique id of a probe
        :param id_: the new id
        :type id_: int
        """
        if not isinstance(id_, int):
            raise TypeError("the id must be a correct integer")
        if id_ <= 0:
            raise ValueError("the id must be a positive integer")
        self.settings["id"] = id_

    def get_slug(self):
        return self.settings["slug"]

    def set_slug(self, slug):
        if not _is_string(slug):
            raise TypeError("the pseudo of plug must be a string")
        self.settings["slug"] = slug

    def get_type(self):
        """get the type of the plug (relay or Energenie)

        Returns:
            string: the type of plug
        """
        return self.settings["type"]

    def set_type(self, type_):
        """set the type of the plug

        Args:
            type_ (string): "energeniee or "relay"

        Raises:
            TypeError: if the type is not a string
            ValueError: if the type differs from "energenie" or "relay"
        """
        if not _is_string(type_):
            raise TypeError("the type must be a string")
        if type_ != "energenie" and type_ != "relay":
            raise ValueError(
                "the type should only be \"energenie\" or \"relay\"")
        self.settings["type"] = type_

    def get_number(self):
        """get the number of the pin for the relay or the channel for the Energenie

        Returns:
            int: number of the pin or channel
        """
        return self.settings["number"]

    def set_number(self, number):
        """set the number of the pin or channel of the plug

        Args:
            number (int): the pin or channel number

        Raises:
            TypeError: the number must be an integer
            ValueError: the channel is between 1 and 4 and pin between 0 and 25
        """
        if not _is_int(number):
            raise TypeError("the channel or pin number should be an integer")
        if self.settings["state"] == "energenie" and number > 4 or number < 1:
            raise ValueError("the channel number should be between 1 and 4")
        elif number > 25:
            raise ValueError("the pin number should be between 0 and 25")
        self.settings["number"] = number

    def get_state(self):
        """get the state of the Plug

        Returns:
            string: "on" if powered or "off" if not
        """
        return self.settings["state"]

    def set_state(self, state):
        """change the value of the state of the plug

        Args:
            state (string): "on" or "off"

        Raises:
            TypeError: the state is a string
            ValueError: if the state differs from "on" or "off"
        """
        if not _is_string(state):
            raise TypeError("the state must be a string of \"on\" or \"off\"")
        if state != "on" and state != "off":
            raise ValueError("the state should only be \"on\" or \"off\"")
        self.settings["state"] = state

    def set_on(self):
        self.set_state("on")

    def set_off(self):
        self.set_state("off")

    def power_on(self):
        electric = Energenie(self.get_number())
        electric.on()
        self.set_on()

    def power_off(self):
        electric = Energenie(self.get_number())
        electric.off()
        self.set_off()


class ThermoPlug(Plug):

    SETTINGS = {"id": 0, "slug": "", "probe": "", "type": "", "number": 0, "state": "off"}

    def __init__(self, settings=SETTINGS):
        super(ThermoPlug, self).__init__(settings)

    def get_probe(self):
        """get the id of the probe used for comparing temps/hygro

        Returns:
            string: the id of the probe
        """
        return self.settings["probe"]

    def set_probe(self, id_):
        """give a new id for the probe used as the indicator
        """
        self.settings["probe"] = id_

    def add_thermo(self, plug_settings):
        plug_settings["thermostat"].append(self.settings)


class LightPlug(Plug):

    SETTINGS = {"id": 0, "slug": "", "type": "", "number": 0, "state": "off", "start": "", "end": ""}

    def __init__(self, settings=SETTINGS):
        super(LightPlug, self).__init__(settings)

    def get_start(self):
        return self.settings["start"]

    def set_start(self, start):
        self.settings["start"] = start

    def get_end(self):
        return self.settings["end"]

    def set_end(self, end):
        self.settings["end"] = end

    def add_light(self, plug_settings):
        plug_settings["lighting"].append(self.settings)


class HygroPlug(Plug):
    pass

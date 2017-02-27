"""
TODO: plug_config.json -> {light:[{id:, slug:, start:, end:, state:}], thermostat:[{}], hygro:[{}]}
    - find a solutin to add the new parameters
"""


from fichier import PlugConfigFile
from gpiozero import Energenie
PATH = "/home/pi/ds18b20_conf/plugs/plug_config.json"


def _is_int(number):
    """check if the type is a int or not


    :param number: the number you want to test
    :type number: object

    :return: True if number is a int
    :rtype: bool
    """
    return isinstance(number, int)


def _is_string(string):
    """check if the type is a string or not

    :param string: the string you want to check
    :type string: object

    :return: True if string is really a string
    :rtype: bool
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

        :return: True if the config exists, false otherwise
        :rtype: bool
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

        :return: the new settings
        :rtype: dict
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
        To add the plug in the settings of the config or overwrite an existing one.
        An id of 0 is recognized as a new Plug to add, the id is set to be of the total number of plugs then

        :param plug: a plug whom config is to add
        :type plug: Plug
        """
        if not isinstance(plug, Plug):
            raise TypeError("no correct plug given")
        id_ = plug.get_id()
        therms = self.get_thermoplugs()
        lights = self.get_lightplugs()
        hygros = self.get_hygroplugs()
        if id_ == 0:
            plug.set_id(len(therms) + len(lights) + len(hygros) + 1)
            if isinstance(plug, ThermoPlug):
                therms.append(plug.settings)
            elif isinstance(plug, LightPlug):
                lights.append(plug.settings)
            elif isinstance(plug, HygroPlug):
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
        """
        Gets the list of all the plugs used as thermostat

        :return: the list of plugs used as thermostat
        :rtype: list
        """
        return self.settings["thermostat"]

    def get_lightplugs(self):
        """
        Gets the list of all the plugs controlling lights

        :return: the list of plugs controlling lights
        :rtype: list
        """
        return self.settings["lighting"]

    def get_hygroplugs(self):
        """
        Gets the list of all the plugs used as hygrostat

        :return: the list of plugs used as hygrostat
        :rtype: list
        """
        return self.settings["hygrostat"]


class Plug:
    """deals with the electric plug Energenie and relay
    """

    def __str__(self, *args, **kwargs):
        state = self.get_state()
        number = self.get_number()
        id = self.get_id()
        return str(id) + ": " + str(number) + " - state: " + state

    def __init__(self, settings):
        self.settings = settings

    def get_id(self):
        """
        Gets the id of the plug (above 1)

        :return: the id of the plug
        :rtype: int
        """
        return self.settings["id"]

    def set_id(self, id_):
        """
        Sets the unique id of a probe (above 1)

        :param id_: the new id
        :type id_: int

        :raises TypeError: if the given id is not an integer
        :raises ValueError: if the given id <= 0
        """
        if not isinstance(id_, int):
            raise TypeError("the id must be a correct integer")
        if id_ <= 0:
            raise ValueError("the id must be a positive integer")
        self.settings["id"] = id_

    def get_slug(self):
        """
        Gets the slug used as a pseudo for the plug

        :return: the slug
        :rtype: str
        """
        return self.settings["slug"]

    def set_slug(self, slug):
        """
        Sets the pseudo of the probe

        :param slug: the new pseudo of the probe
        :type slug: str

        :raises TypeError: If the given slug is not a string
        """
        if not _is_string(slug):
            raise TypeError("the pseudo of plug must be a string")
        self.settings["slug"] = slug

    def get_type(self):
        """get the type of the plug (relay or Energenie)

        :return: the type of plug
        :rtype: str
        """
        return self.settings["type"]

    def set_type(self, type_):
        """set the type of the plug

        :param type_: "energenie" or "relay"
        :type type_: str

        :raises TypeError: if the type is not a string
        :raises ValueError: if the type differs from "energenie" or "relay"
        """
        if not _is_string(type_):
            raise TypeError("the type must be a string")
        if type_ != "energenie" and type_ != "relay":
            raise ValueError(
                "the type should only be \"energenie\" or \"relay\"")
        self.settings["type"] = type_

    def get_number(self):
        """get the number of the pin for the relay or the channel for the Energenie

        :return: number of the pin or channel
        :rtype: int
        """
        return self.settings["number"]

    def set_number(self, number):
        """set the number of the pin or channel of the plug

        :param number: the new pin or channel number
        :type number: int

        :raises TypeError: the number must be an integer
        :raises ValueError: the channel is between 1 and 4 and pin in [5, 6, 13, 16, 23, 26, 22, 24, 27, 12]
        """
        if not _is_int(number):
            raise TypeError("the channel or pin number should be an integer")
        if self.settings["state"] == "energenie" and number > 4 or number < 1:
            raise ValueError("the channel number should be between 1 and 4")
        elif number not in [5, 6, 13, 16, 23, 26, 22, 24, 27, 12]:
            raise ValueError("the pin number should be either 5, 6, 13, 16, 22, 23, 24, 26, 27 or 12")
        self.settings["number"] = number

    def get_state(self):
        """get the state of the Plug

        :return: "on" if powered or "off" if not
        :rtype: str
        """
        return self.settings["state"]

    def set_state(self, state):
        """change the value of the state of the plug

        :param state: "on" or "off"
        :type state: str

        :raises TypeError: the state is a string
        :raises ValueError: if the state differs from "on" or "off"
        """
        if not _is_string(state):
            raise TypeError("the state must be a string of \"on\" or \"off\"")
        if state != "on" and state != "off":
            raise ValueError("the state should only be \"on\" or \"off\"")
        self.settings["state"] = state

    def set_on(self):
        """
        Sets the state to on
        """
        self.set_state("on")

    def set_off(self):
        """
        Sets the state to off
        """
        self.set_state("off")

    def power_on(self):
        if self.get_type() == "energenie":
            electric = Energenie(self.get_number())
            electric.on()
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            number = self.get_number()
            GPIO.setup(number, GPIO.OUT)
            GPIO.output(number, GPIO.LOW)
        self.set_on()

    def power_off(self):
        if self.get_type() == "energenie":
            electric = Energenie(self.get_number())
            electric.off()
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            number = self.get_number()
            GPIO.setup(number, GPIO.OUT)
            GPIO.output(number, GPIO.HIGH)
        self.set_off()


class ThermoPlug(Plug):

    SETTINGS = {"id": 0, "slug": "", "probe": "", "type": "", "number": 0, "state": "off"}

    def __init__(self, settings=SETTINGS):
        super(ThermoPlug, self).__init__(settings)

    def get_probe(self):
        """get the id of the probe used for comparing temps/hygro

        :returns: the id of the probe
        :rtype: str
        """
        return self.settings["probe"]

    def set_probe(self, id_):
        """
        give a new id for the probe used as the indicator

        :param id_: the id correspond to the slug of the probe
        :type id_: str
        """
        self.settings["probe"] = id_


class LightPlug(Plug):

    SETTINGS = {"id": 0, "slug": "", "type": "", "number": 0, "state": "off", "start": "", "end": ""}

    def __init__(self, settings=SETTINGS):
        super(LightPlug, self).__init__(settings)

    def get_start(self):
        """
        Gets the starting time for the light (HH:MM)

        :return: the starting time (HH:MM)
        :rtype: str
        """
        return self.settings["start"]

    def set_start(self, start):
        """
        Sets the starting time for the light (HH:MM)

        :param start: HH:MM
        :type start: str
        """
        self.settings["start"] = start

    def get_end(self):
        """
        Gets the ending time for the light (HH:MM)

        :return: the ending time (HH:MM)
        :rtype: str
        """
        return self.settings["end"]

    def set_end(self, end):
        """
        Sets the starting time for the light (HH:MM)

        :param end: HH:MM
        :type end: str
        """
        self.settings["end"] = end


class HygroPlug(Plug):
    pass

from fichier import PlugConfigFile

SETTINGS = {"probe": "", "type": "", "number": 0, "state": "off"}


def _is_int(self, number):
    """check if the type is a int or not

    Args:
        number (any): the number you want to test

    Returns:
        bool: True if number is a int
    """
    return isinstance(number, int)


def _is_string(self, string):
    """check if the type is a string or not

    Args:
        string (any): the string you want to check

    Returns:
        bool: True if string is really a string
    """
    return isinstance(string, str)


class Plug():
    """deals with the electric plug Energenie and relay
    """

    def __init__(self, slug, settings=SETTINGS):
        self.settings = settings
        self.slug = slug
        self.path = "/home/pi/ds18b20_conf/" + self.idt + ".json"
        self.config = PlugConfigFile(self.path)

    def get_probe(self):
        """get the id of the probe used for comparing temps/hygro

        Returns:
            String: the id of the probe
        """
        pass

    def set_probe(self):
        """give a new id for the probe used as the indicator
        """
        pass

    def get_type(self):
        """get the type of the plug (relay or Energenie)

        Returns:
            String: the type of plug
        """
        pass

    def set_type(self, type_):
        """set the type of the plug

        Args:
            type_ (String): "energeniee or "relay"

        Raises:
            ValueError: if the type differs from "energenie" or "relay"
        """
        if not _is_string(type_):
            raise TypeError("the type must be a string")
        if type_ != "energenie" or type_ != "relay":
            raise ValueError(
                "the type should only be \"energenie\" or \"relay\"")
        self.settings["type"] = type_

    def get_number(self):
        """get the number of the pin for the relay or the channel for the Energenie

        Returns:
            Int: number of the pin or channel
        """
        pass

    def set_number(self, number):
        """set the number of the pin or channel of the plug

        Args:
            number (Int): the pin or channel number

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
            String: "on" if porwered or "off" if not
        """
        pass

    def set_state(self, state):
        """change the value of the state of the plug

        Args:
            state (String): "on" or "off"

        Raises:
            TypeError: the state is a string
            ValueError: if the state differs from "on" or "off"
        """
        if not _is_string(state):
            raise TypeError("the state must be a string of \"on\" or \"off\"")
        if state != "on" or state != "off":
            raise ValueError("the state should only be \"on\" or \"off\"")
        self.settings["state"] = state

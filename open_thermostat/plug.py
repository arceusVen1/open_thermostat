
SETTINGS = {"probe": "", "type": "", "number": 0, "state": "off"}


class Plug():
    """deals with the electric plug Energenie and relay
    """

    def __init__(self, settings=SETTINGS):
        self.settings = settings

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
        if not isinstance(number, int):
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
            ValueError: if tge state differs from "on" or "off"
        """
        if state != "on" or state != "off":
            raise ValueError("the state should only be \"on\" or \"off\"")
        self.settings["state"] = state

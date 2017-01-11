from open_ds18b20.probe import Probe
from plug import LightPlug
from datetime import datetime


def _compare_time(range_):
    time = datetime.now()
    moments = []
    for moment in range_:
        moment = datetime.strptime(moment, "%H:%M")
        moments.append(moment)
        if moment.hour <= time.hour and moment.minute <= time.minute:
            return moment
    moments.sort()
    return moments[-1]


class Thermostat:
    def __init__(self, temperatures, step=1):
        """get the probe ids and their temps in 2 different lists

        Args:
            temperatures (dict): {id_of_the_probe: temp}
            step (int, optional): the range above and below the ref temp accepted, 1 by default
        """
        self.ids = list(temperatures.keys())
        self.temperatures = list(temperatures.values())
        self.step = step

    def need_action(self):
        """Take a look at the configuration of the plugs and compares with the temps to decide if an action is needed (on/off)

        Returns:
            dict: {id_of_the_probe : action}
        """
        actions = {}
        for i in range(len(self.ids)):
            probe = Probe(self.ids[i])
            if probe.has_config():
                probe.get_data()
                if probe.is_thermostated():
                    thermorange = probe.link_moment_temp()
                    moment = _compare_time(thermorange)
                    ref = thermorange[datetime.strftime(moment, "%H:%M")]
                    temp = float(self.temperatures[i])
                    if temp > (ref + self.step):
                        actions[self.ids[i]] = "off"
                    elif temp < (ref - self.step):
                        actions[self.ids[i]] = "on"
        return actions


class Lightstat:
    def __init__(self, plugs):
        """

        :type plugs: list
        """
        self.plugs = plugs

    @property
    def plugs(self):
        return self.plugs

    @plugs.setter
    def plugs(self, plugs):
        if not isinstance(plugs, list):
            raise TypeError("you need a list of plugs")
        for plug in plugs:
            if not isinstance(plug, LightPlug):
                raise TypeError("the plugs must be from LightPlug")
        self.plugs = plugs

    def action(self):
        for plug in self.plugs:
            range_ = []
            range_.append(plug.get_start())
            range_.append(plug.get_end())
            time = _compare_time(range_)
            time = datetime.strftime(time, "%H:%M")
            if time == plug.get_start():
                plug.power_on()
            else:
                plug.power_off()


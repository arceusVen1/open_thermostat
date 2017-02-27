from open_ds18b20.probe import Ds18b20, Dht22, Materials
from plug import LightPlug
from datetime import datetime


def _compare_time(range_):
    """
    Compares a list of moments (format HH:MM) with the current time by returning the first moment that is
    before the current time. If no moment found, returns the last moment in time from a sorted list
    of datetime to avoid conflict with morning.

    :param range_: the list of moment to compare
    :type range_: list

    :return: the first moment before current time
    :rtype: Datetime
    """
    time = datetime.now()
    moments = []
    for moment in range_:
        moment = datetime.strptime(moment, "%H:%M")
        if moment.hour <= time.hour and moment.minute <= time.minute:
            return moment
        moments.append(moment)
    moments.sort()
    return moments[-1]


class Thermostat:
    def __init__(self, temperatures, step=1):
        """
        Gets the probe slugs and their temps in 2 different lists

        :param temperatures:  hash of temps from open_ds18b20 return {slug_of_the_probe: temp}
        :type temperatures: dict
        :param: (optional) the range above and below the ref temp accepted, 1 by default
        :type step: int
        """
        self.slugs = list(temperatures.keys())
        self.temperatures = list(temperatures.values())
        self.step = step

    def need_action(self):
        """
        Takes a look at the configuration of the probes and
        compares with the temperatures to decide if an action is needed (on/off)

        :returns: {slug_of_the_probe : action}
        :rtype: dict
        """
        actions = {}
        materials = Materials()
        materials.allow_config()
        materials.get_data()
        for i in range(len(self.slugs)):
            fprobe = materials.get_ds18b20_by_slug(self.slugs[i])
            print(fprobe)
            if fprobe is not (None, None):
                probe = Ds18b20(settings=fprobe[0])
                if probe.has_config(materials) and probe.is_thermostated():
                    thermorange = probe.link_moment_value()
                    moment = _compare_time(list(thermorange.keys()))
                    ref = thermorange[datetime.strftime(moment, "%H:%M")]
                    temp = float(self.temperatures[i])
                    if temp > (ref + self.step):
                        actions[self.slugs[i]] = "off"
                    elif temp < (ref - self.step):
                        actions[self.slugs[i]] = "on"
        return actions


class Lightstat:
    def __init__(self, plugs):
        """
        :param plugs: the list of plugs connected to light
        :type plugs: list
        """
        self.plugs = plugs

    @property
    def plugs(self):
        return self._plugs

    @plugs.setter
    def plugs(self, plugs):
        if not isinstance(plugs, list):
            raise TypeError("you need a list of plugs")
        for plug in plugs:
            if not isinstance(plug, LightPlug):
                raise TypeError("the plugs must be from LightPlug")
        self._plugs = plugs

    def action(self):
        """
        Powers on or off the plugs based on their configuration and current time
        """
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


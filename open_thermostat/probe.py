from open_ds18b20.probe import Probe
from datetime import datetime


class Thermostat():

    def __init__(self, temperatures, step=1):
        """get the probe ids and thier temps in 2 different lists

        Args:
            temperatures (dict): {id_of_the_probe: temp}
            step (int, optional): the range above and below the ref temp accepted, 1 by default
        """
        self.ids = list(temperatures.keys())
        self.temperatures = list(temperatures.values())
        self.step = step

    def need_action(self):
        actions = {}
        for i in range(len(self.ids)):
            probe = Probe(self.ids[i])
            if probe.has_config():
                probe.get_data()
                if probe.is_thermostated():
                    thermorange = probe.link_moment_temp()
                    # do somethig to get time and temp
                    moment = self._compare_time(thermorange)
                    ref = thermorange[moment]
                    temp = float(self.temperatures[i])
                    if temp > (ref + self.step):
                        actions[self.ids[i]] = "off"
                    elif temp < (ref - self.step):
                        actions[self.ids[i]] = "on"
        return actions

    def _compare_time(self, thermorange):
        time = datetime.now()
        for moment in thermorange:
            moment = datetime.strptime(moment, "%H:%M")
            if moment.hour <= time.hour and moment.minute <= time.minute:
                return moment

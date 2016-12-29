from open_thermostat.plug import Plug
from open_thermostat.thermostat import Thermostat
from open_thermostat.fichier import PlugConfigFile


def get_temp():
	pass

def main():
	temp = get_temp()
	thermostat = Thermostat(temp)
	actions = thermostat.need_action()
	probes = list(actions.keys())
	
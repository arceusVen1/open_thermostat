from open_thermostat.plug import Plug, Materials
from open_thermostat.thermostat import Thermostat
from open_ds18b20.__main__ import main as acqtemp

def get_temp():
    temp, result = acqtemp()
    return temp

def take_action(thermostat, plug, action):
    if action == "on":
        thermostat.power_on(plug)
    else:
        thermostat.power_off(plug)

def main():
    temp = get_temp()
    thermostat = Thermostat(temp)
    actions = thermostat.need_action()
    probes = list(actions.keys())
    materials = Materials().detect_plugs()
    plugs = []
    for material in materials.files:
        plug = Plug(material)
        plugs.append(plug)
        if plug.has_config():
            plug.get_data()
            if plug.get_probe() in probes:
                take_action(plug, actions[plug.get_probe()])
    return



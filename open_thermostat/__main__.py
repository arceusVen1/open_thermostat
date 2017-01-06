from plug import ThermoPlug, LightPlug, Materials
from thermostat import Thermostat, Lightstat
from open_ds18b20.__main__ import main as acqtemp


def get_temp():
    temp, result = acqtemp()
    return temp


def take_action(plug, action):
    if action == "on":
        plug.power_on()
    else:
        plug.power_off()


def main():
    temp = get_temp()
    thermostat = Thermostat(temp)
    actions = thermostat.need_action()
    probes = list(actions.keys())
    materials = Materials()
    materials.get_data()
    plugs = []
    for thermo_plug in materials.settings["thermostat"]:
        plug = ThermoPlug(thermo_plug)
        plugs.append(plug)
        if plug.get_probe() in probes:
                take_action(plug, actions[plug.get_probe()])
    light_plugs = []
    for light_plug in materials.settings["light"]:
        light_plugs.append(LightPlug(light_plug))
    Lightstat(light_plugs).actions()
    return

if __name__ == '__main__':
    main()

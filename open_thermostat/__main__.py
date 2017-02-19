from open_thermostat.plug import ThermoPlug, LightPlug, Materials
from open_thermostat.thermostat import Thermostat, Lightstat
from open_ds18b20.__main__ import main as acqtemp


def get_temp():
    result = acqtemp()
    return result[0]


def take_action(plug, action):
    """
    Powers on or off a plug based on the action required

    :param plug: the plug to Power on or off
    :type plug: Plug
    :param action: "on" or "off", it is the given result of Thermostat.need_action() function
    :type action: str
    """
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
    for light_plug in materials.settings["lighting"]:
        light_plugs.append(LightPlug(light_plug))
    Lightstat(light_plugs).action()
    return

if __name__ == '__main__':
    main()

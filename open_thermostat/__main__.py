from plug import Plug, Materials
from thermostat import Thermostat
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
    print(actions)
    probes = list(actions.keys())
    materials = Materials()
    materials.detect_plugs()
    plugs = []
    for material in materials.files:
        plug = Plug(material)
        plugs.append(plug)
        if plug.has_config():
            plug.get_data()
            print(plug.get_probe())
            if plug.get_probe() in probes:
                print("ok")
                take_action(thermostat, plug, actions[plug.get_probe()])
    return

if __name__ == '__main__':
    main()

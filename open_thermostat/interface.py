# Imports-------------------------------------------------

import sys
from plug import *

# GLOBAL--------------------------------------------------

PROMPT = '> '


# ---------------------------------------------------------

def display(string):
    sys.stdout.write(str(string) + "\n")


def show_plugs():
    materials = Materials()
    if materials.has_config():
        materials.get_data()
        display("List of plugs")
    else:
        display("no config yet")
        return
    i = 1
    display("Plugs for thermostat")
    plugs = []
    thermoplugs = materials.get_thermoplugs()
    lightplugs = materials.get_lightplugs()
    for therm in thermoplugs:
        plug = ThermoPlug(therm)
        plugs.append(plug)
        display(str(i) + " : " + plug.get_slug())
        i += 1
    display("Plugs for lighting")
    for light in lightplugs:
        plug = LightPlug(light)
        plugs.append(plug)
        display(str(i) + " : " + plug.get_slug())
        i += 1
    display("Would you like to configure one or add one ? (y/new/n)")
    choice = input(PROMPT)
    if choice == "new":
        plug = None
    elif choice == "y":
        display("which one ?")
        choice = int(input(PROMPT))
        if choice > i or choice < 1:
            return "not a correct probe"
        else:
            plug = plugs[choice - 1]
    else:
        return
    show_config_plug(plug)
    config_plug(materials.settings, plug)


def show_config_plug(plug):
    if not isinstance(plug, Plug):
        display("no confg for this plug")
        return
    display("- slug : " + plug.get_slug())
    display("- type : " + plug.get_type())
    display("- number : " + plug.get_number())
    display("- state : " + plug.get_state())
    if isinstance(plug, ThermoPlug):
        display("- probe : " + plug.get_probe())
    if isinstance(plug, LightPlug):
        display("- start : " + plug.get_start)
        display("- end : " + plug.get_end())


def config_plug(settings, plug=None):
    if plug is None or not isinstance(plug, Plug):
        display("For thermostat or light ? (1/2)")
        choice = int(input(PROMPT))
        if choice == 1:
            plug = ThermoPlug()
        elif choice == 2:
            plug = LightPlug()
        else:
            display("uncorrect choice")
            return
    flag = False
    while not flag:
        display("new slug :")
        try:
            plug.set_slug(input(PROMPT))
            flag = True
        except Exception as e:
            display(str(e))
    flag = False
    while not flag:
        display("new type :")
        try:
            plug.set_type(input(PROMPT))
            flag = True
        except Exception as e:
            display(str(e))
    flag = False
    while not flag:
        display("new number ?")
        try:
            plug.set_number(int(input(PROMPT)))
            flag = True
        except Exception as e:
            display(str(e))
    flag = False
    if isinstance(plug, ThermoPlug):
        while not flag:
            display("pseudo of the probe")
            try:
                plug.set_probe(input(PROMPT))
                flag = True
            except Exception as e:
                display(str(e))
        plug.add_thermo(settings)
    elif isinstance(plug, LightPlug):
        while not flag:
            display("time of power on (HH:MM)")
            try:
                plug.set_start(input(PROMPT))
                flag = True
            except Exception as e:
                display(str(e))
        flag = False
        while not flag:
            display("time of power off (HH:MM)")
            try:
                plug.set_end(input(PROMPT))
                flag = True
            except Exception as e:
                display((str(e)))
        plug.add_light(settings)

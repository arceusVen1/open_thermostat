# Imports-------------------------------------------------

import sys
from plug import *

PROMPT = '> '


# ---------------------------------------------------------

def display(string):
    sys.stdout.write(str(string) + "\n")


def show_plugs():
    materials = Materials()
    if materials.has_config():
        materials.get_data()
        display("Liste des prises")
    else:
        display("Aucune configuration disponible")
        return
    i = 1
    display("Prises de thermostats")
    plugs = []
    thermoplugs = materials.get_thermoplugs()
    lightplugs = materials.get_lightplugs()
    for therm in thermoplugs:
        plug = ThermoPlug(therm)
        plugs.append(plug)
        display(str(i) + " : " + plug.get_slug())
        i += 1
    display("Prise d'éclairage")
    for light in lightplugs:
        plug = LightPlug(light)
        plugs.append(plug)
        display(str(i) + " : " + plug.get_slug())
        i += 1
    display("Souhaitez vous configurer une prise ou en ajouter une ? (o/a/n)")
    choice = input(PROMPT)
    if choice == "a":
        plug = None
    elif choice == "o":
        display("Laquelle ?")
        choice = int(input(PROMPT))
        if choice > i or choice < 1:
            return "Choix incorrect"
        else:
            plug = plugs[choice - 1]
    else:
        return
    show_config_plug(plug)
    config_plug(materials, plug)


def show_config_plug(plug):
    if not isinstance(plug, Plug):
        display("Aucune configuration pour cette prise")
        return
    display("- pseudo : " + plug.get_slug())
    display("- type : " + plug.get_type())
    display("- pin/channel : " + str(plug.get_number()))
    display("- état : " + plug.get_state())
    if isinstance(plug, ThermoPlug):
        display("- sonde : " + plug.get_probe())
    if isinstance(plug, LightPlug):
        display("- début : " + plug.get_start())
        display("- fin : " + plug.get_end())


def config_plug(materials, plug=None):
    if plug is None or not isinstance(plug, Plug):
        display("Prise de thermostat ou éclairage ? (1/2)")
        choice = int(input(PROMPT))
        if choice == 1:
            plug = ThermoPlug()
        elif choice == 2:
            plug = LightPlug()
        else:
            display("choix incorrect")
            return
    flag = False
    while not flag:
        display("Nouveau pseudo :")
        try:
            plug.set_slug(input(PROMPT))
            flag = True
        except Exception as e:
            display(str(e))
    flag = False
    while not flag:
        display("Nouveau type (energenie/relay):")
        try:
            plug.set_type(input(PROMPT))
            flag = True
        except Exception as e:
            display(str(e))
    flag = False
    while not flag:
        display("Nouveau pin/channel ?")
        try:
            plug.set_number(int(input(PROMPT)))
            flag = True
        except Exception as e:
            display(str(e))
    flag = False
    if isinstance(plug, ThermoPlug):
        while not flag:
            display("Pseudo de la sonde associée")
            try:
                plug.set_probe(input(PROMPT))
                flag = True
            except Exception as e:
                display(str(e))
    elif isinstance(plug, LightPlug):
        while not flag:
            display("Heure d'allumage (HH:MM)")
            try:
                plug.set_start(input(PROMPT))
                flag = True
            except Exception as e:
                display(str(e))
        flag = False
        while not flag:
            display("Heure d'extinction (HH:MM)")
            try:
                plug.set_end(input(PROMPT))
                flag = True
            except Exception as e:
                display((str(e)))
    materials.add_plug(plug)
    materials.set_data()

show_plugs()
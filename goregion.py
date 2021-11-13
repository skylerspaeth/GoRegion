#!/usr/bin/env python3

#ensure compatible interpreter version
import sys
if (sys.version_info[0] < 3):
    raise Exception("This script requires Python 3, while you ran it with {}.{}.".format(sys.version_info[0], sys.version_info[1]))

#JSON manipulation and requests module imports
import json
from urllib.request import urlopen

#needed for iptables invocation
import os

#Valve physical network diagram path
networkDiagramPath = "airports.json"

#iptables interface function
def iptc(operation, addresses):

    if (operation == "setupChain"):
        print("Creating iptables chain \"goregion\"...")
        tableCreateCode = 0 if chainPresent else os.system("sudo iptables -N goregion")
        tableBindCode = 0 if chainBound else os.system("sudo iptables -A INPUT -j goregion")
        print("Successfully created chain." if tableCreateCode == 0 and tableBindCode == 0 else "Error creating chain.")

    elif (operation == "block"):
        print("Blocking the following addresses not contained within selected region:", ", ".join(addresses))
        for address in addresses:
            os.system("sudo iptables -A goregion -s {} -j DROP".format(address))

    elif (operation == "allow"):
        print("Unblocking the following addresses:", ", ".join(addresses))
        for address in addresses:
            os.system("sudo iptables -D goregion -s {} -j DROP".format(address))

    elif (operation == "reset"):
        print("Resetting all goregion rules...")
        print("Successfully reset chain." if os.system("sudo iptables -F goregion") == 0 else "Error resetting chain.")

#check if iptables chain exists and create it if not
chainPresent = True if os.system("sudo iptables -S | grep -Fx -- '-N goregion'") == 0 else False
chainBound = True if os.system("sudo iptables -S | grep -Fx -- '-A INPUT -j goregion'") == 0 else False
chainSetup = True if chainPresent and chainBound else False
if not chainSetup:
    print("Chain not setup, triggered by values chainPresent: {} and chainBound: {}.".format(chainPresent, chainBound))
    iptc("setupChain", None)

iptc("reset", None)

with urlopen("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json") as jsonResponse:
    data = json.loads(jsonResponse.read())
    allRelays = data["pops"]
    print("Retrieved SteamDB NetworkDatagramConfig.json version {}.".format(data.get("revision")))


    with open(networkDiagramPath, "r") as networkDiagramData:
        networkDiagramJSON = json.loads(networkDiagramData.read())
        print("The latest available region codes are as follows:")
        validRegions = list(map(lambda x: x, networkDiagramJSON.get("regions").keys()))
        validRegionsStr = ", ".join(validRegions).upper()
        print(validRegionsStr)

        selectedRegion = input("Select a region by entering its code: ").lower()
        if selectedRegion in validRegions:
            regionalCities = list(map(lambda x: x, networkDiagramJSON.get("regions").get(selectedRegion).get("cities")))
            citiesToDisplay = ", ".join(list(map(lambda x: "{} ({})".format(x.get("cityName"), x.get("airportCode").upper()), regionalCities)))
            print("Cities available in the {} region: {}".format(selectedRegion.upper(), citiesToDisplay))

            valveRelayNames = list(allRelays.keys())
            valveRelays = list(allRelays.values())

            def callback(currentRelay):
                if currentRelay.get("referrers"):
                    return currentRelay["referrers"]
                else:
                    return currentRelay["airportCode"]

            relaysInRegion = list(map(callback, networkDiagramJSON["regions"][selectedRegion]["cities"]))
            print(relaysInRegion)
            #should this be an array instead of list?
            blacklistAddresses = []

            for (relayName, relay) in zip(valveRelayNames, valveRelays):
                if relay.get("relays"):
                    if relayName not in relaysInRegion:
                        for address in map(lambda x: x["ipv4"], relay["relays"]):
                            blacklistAddresses.append(address)

            iptc("block", blacklistAddresses)

        else:
            print("You must enter a valid region from the following:", validRegionsStr)

print("Thank you for using CS:GO region selector.")
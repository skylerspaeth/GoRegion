#!/usr/bin/env python3

#ensure compatible interpreter version
import sys
if (sys.version_info[0] < 3):
    raise Exception("This script requires Python 3, while you ran it with {}.{}.".format(sys.version_info[0], sys.version_info[1]))

#JSON manipulation and requests module imports
import json
import urllib.request
import itertools

#needed for iptables invocation
import os

#Valve physical network diagram path
NETWORK_DIAGRAM_PATH = "layout.json"

#iptables interface functions
def callIpTables(args):
    return os.system("sudo iptables {}".format(args))

def iptc(operation, addresses):

    if (operation == "setupChain"):
        print("Creating iptables chain \"goregion\"...")
        tableCreateCode = 0 if chainPresent else callIpTables("-N goregion")
        tableBindCode = 0 if chainBound else callIpTables("-A INPUT -j goregion")
        print("Successfully created chain." if tableCreateCode == 0 and tableBindCode == 0 else "Error creating chain.")

    elif (operation == "block"):
        print("Blocking the following addresses not contained within selected region:", ", ".join(addresses))
        for address in addresses:
            callIpTables("-A goregion -s {} -j DROP".format(address))

    elif (operation == "allow"):
        print("Unblocking the following addresses:", ", ".join(addresses))
        for address in addresses:
            callIpTables("-D goregion -s {} -j DROP".format(address))

    elif (operation == "reset"):
        print("Resetting all goregion rules...")
        print("Successfully reset chain." if callIpTables("-F goregion") == 0 else "Error resetting chain.")

#check if iptables chain exists and create it if not
chainPresent = True if callIpTables("-S | grep -Fx -- '-N goregion'") == 0 else False
chainBound = True if callIpTables("-S | grep -Fx -- '-A INPUT -j goregion'") == 0 else False
chainSetup = True if chainPresent and chainBound else False
if not chainSetup:
    print("Chain not setup, triggered by values chainPresent: {} and chainBound: {}.".format(chainPresent, chainBound))
    iptc("setupChain", None)

iptc("reset", None)

with urllib.request.urlopen("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json") as rawData:
    jsonData = json.loads(rawData.read())
    allPops = jsonData["pops"]
    print("Retrieved SteamDB NetworkDatagramConfig.json version {}.".format(jsonData.get("revision")))


    with open(NETWORK_DIAGRAM_PATH, "r") as networkDiagramData:
        networkDiagramJSON = json.loads(networkDiagramData.read())
        print("The latest available region codes are as follows:")
        validRegions = networkDiagramJSON.get("regions").keys()
        validRegionsStr = ", ".join(validRegions).upper()
        print(validRegionsStr)

        selectedRegion = input("Select a region by entering its code: ").lower()
        if selectedRegion not in validRegions:
            print("You must enter a valid region from the following:", validRegionsStr)
        else:
            regionalCities = networkDiagramJSON["regions"][selectedRegion]["cities"]
            citiesToDisplay = ", ".join([
                "{} ({})".format(city.get("cityName"), city.get("airportCode").upper())
                for city in regionalCities
            ])
            print("Cities available in the {} region: {}".format(selectedRegion.upper(), citiesToDisplay))

            popsInRegion = list(itertools.chain(*[city.get("referrers", [city.get("airportCode")]) for city in regionalCities]))
            print("POPs in region:", popsInRegion)

            blacklistAddresses = []
            for (popName, pop) in allPops.items():
                if pop.get("relays"):
                    if popName not in popsInRegion:
                        for address in [relay["ipv4"] for relay in pop["relays"]]:
                            blacklistAddresses.append(address)

            iptc("block", blacklistAddresses)

print("Thank you for using CS:GO region selector.")

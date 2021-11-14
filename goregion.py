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

#iptables interface class
class ipTablesControl:
    @staticmethod
    def callIpTables(args):
        return os.system("sudo iptables {}".format(args))

    @classmethod
    def createChain(cls):
        print("Creating iptables chain \"goregion\"...")
        exitCode = cls.callIpTables("-N goregion")
        print("Successfully created chain." if exitCode == 0 else "Error creating chain.")

    @classmethod
    def bindChain(cls):
        print("Binding iptables chain \"goregion\" so it's passed traffic from default INPUT chain...")
        cls.callIpTables("-A INPUT -j goregion")
        print("Successfully bound chain." if exitCode == 0 else "Error binding chain.")

    @classmethod
    def block(cls, addresses):
        print("Blocking the following addresses not contained within selected region:", ", ".join(addresses))
        for address in addresses:
            cls.callIpTables("-A goregion -s {} -j DROP".format(address))

    @classmethod
    def allow(cls, addresses):
        print("Unblocking the following addresses:", ", ".join(addresses))
        for address in addresses:
            cls.callIpTables("-D goregion -s {} -j DROP".format(address))

    @classmethod 
    def reset(cls):
        print("Resetting all goregion rules...")
        print("Successfully reset chain." if cls.callIpTables("-F goregion") == 0 else "Error resetting chain.")

#check if iptables chain exists and create it if not
chainPresent = ipTablesControl.callIpTables("-S | grep -Fx -- '-N goregion'") == 0
chainBound = ipTablesControl.callIpTables("-S | grep -Fx -- '-A INPUT -j goregion'") == 0
chainSetup = chainPresent and chainBound
if not chainSetup:
    print("Chain not setup, triggered by values chainPresent: {} and chainBound: {}.".format(chainPresent, chainBound))
    ipTablesControl.createChain()
    ipTablesControl.bindChain()

ipTablesControl.reset()

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

            ipTablesControl.block(blacklistAddresses)

print("Thank you for using CS:GO region selector.")

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
        print(colors.write("cyan", "Successfully created chain.") if exitCode == 0 else colors.write("fail", "Error creating chain."))

    @classmethod
    def bindChain(cls):
        print("Binding iptables chain \"goregion\" so it's passed traffic from default INPUT chain...")
        exitCode = cls.callIpTables("-A INPUT -j goregion")
        print(colors.write("cyan", "Successfully bound chain.") if exitCode == 0 else colors.write("fail", "Error binding chain."))

    @classmethod
    def block(cls, addresses):
        print(colors.write("blue", "Blocking ") \
        + colors.write("blue", colors.write("bold", str(len(addresses)))) \
        + colors.write("blue", " addresses not contained within selected region..."))
        for address in addresses:
            exitCode = cls.callIpTables("-A goregion -s {} -j DROP".format(address))
            if exitCode != 0:
                raise Exception("Error while trying to append DROP rule for {}. ".format(address) \
                + "There's likely an issue with iptables or the address and we don't want to break anything by continuing.")
        print(colors.write("green", "IP tables rules appended, hosts successfully blocked."))

    @classmethod
    def allow(cls, addresses):
        print("Unblocking the following addresses:", ", ".join(addresses))
        for address in addresses:
            cls.callIpTables("-D goregion -s {} -j DROP".format(address))

    @classmethod 
    def reset(cls):
        print("Resetting all goregion rules...")
        print(colors.write("cyan", "Successfully reset chain.") if cls.callIpTables("-F goregion") == 0 else colors.write("fail", "Error resetting chain."))

#text coloring class for better readability
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    #COLOR REFERENCE:
    #cyan is for setup/anything before the process of blocking addresses, blue is for anything after, and green is final success.

    @classmethod
    def write(cls, color, text):
        return getattr(cls, color.upper()) + text + cls.ENDC

#check if iptables chain exists and create it if not
chainPresent = ipTablesControl.callIpTables("-S | grep -Fx -- '-N goregion' > /dev/null") == 0
chainBound = ipTablesControl.callIpTables("-S | grep -Fx -- '-A INPUT -j goregion' > /dev/null") == 0
chainSetup = chainPresent and chainBound
if not chainSetup:
    print(colors.write("warning", "\"goregion\" chain not found, attempting to setup..."))
    ipTablesControl.createChain()
    ipTablesControl.bindChain()

ipTablesControl.reset()

with urllib.request.urlopen("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json") as rawData:
    jsonData = json.loads(rawData.read())
    allPops = jsonData["pops"]
    print(colors.write("green", "Retrieved SteamDB NetworkDatagramConfig.json version {}.\n".format(jsonData.get("revision"))))

    with open(NETWORK_DIAGRAM_PATH, "r") as networkDiagramData:
        networkDiagramJSON = json.loads(networkDiagramData.read())
        print("The latest available region codes are as follows:")
        validRegions = networkDiagramJSON["regions"].keys()
        validRegionsStr = ", ".join(validRegions).upper()
        print(validRegionsStr)

        selectedRegion = input("Select a region by entering its code: ").lower()
        if selectedRegion not in validRegions:
            print(colors.write("fail", "You must enter a valid region from the following: " + validRegionsStr))
        else:
            regionalCities = networkDiagramJSON["regions"][selectedRegion]["cities"]
            citiesToDisplay = ", ".join([
                "{} ({})".format(city.get("cityName"), city.get("airportCode").upper())
                for city in regionalCities
            ])
            print("\nRegion {} contains the following cities: {}".format(selectedRegion.upper(), citiesToDisplay))

            popsInRegion = list(itertools.chain(*[city.get("referrers", [city.get("airportCode")]) for city in regionalCities]))

            blacklistAddresses = []
            for (popName, pop) in allPops.items():
                if pop.get("relays") and popName not in popsInRegion:
                    for address in [relay["ipv4"] for relay in pop["relays"]]:
                        blacklistAddresses.append(address)

            ipTablesControl.block(blacklistAddresses)

print("Thank you for using CS:GO region selector.")

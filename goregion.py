#!/usr/bin/env python3
#ensure compatible interpreter version
import sys
if (sys.version_info[0] < 3):
    raise Exception("This script requires Python 3, while you ran it with {}.{}.".format(sys.version_info[0], sys.version_info[1]))

#goregion version and release date metadata
__version__ = "0.2.0"
__date__ = "19 January 2022"

#module for handling arguments
import argparse

#JSON manipulation and requests module imports
import json
import urllib.request
import itertools

#iptables invocation and related module for data validation
import os
from validate import validate

#text coloring class for better readability
from decorate import Colors

#setup ping and reset optional arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ping", help="print latency to each region", action="store_true")
parser.add_argument("-r", "--reset", help="resets goregion's iptables chain, allowing all regions again", action="store_true")
parser.add_argument("-v", "--version", help="check installed goregion version", action="store_true")
args = parser.parse_args()

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
        print(Colors.write("cyan", "Successfully created chain.") if exitCode == 0 else Colors.write("fail", "Error creating chain."))

    @classmethod
    def bindChain(cls):
        print("Binding iptables chain \"goregion\" so it's passed traffic from default INPUT chain...")
        exitCode = cls.callIpTables("-A INPUT -j goregion")
        print(Colors.write("cyan", "Successfully bound chain.") if exitCode == 0 else Colors.write("fail", "Error binding chain."))

    @classmethod
    def block(cls, addresses):
        print(Colors.write("blue", "Blocking ") \
        + Colors.write("blue", Colors.write("bold", str(len(addresses)))) \
        + Colors.write("blue", " addresses not contained within selected region..."))
        for address in addresses:
            if validate(address):
                exitCode = cls.callIpTables("-A goregion -s {} -j DROP".format(address))
                if exitCode != 0:
                    raise Exception("Error while trying to append DROP rule for {}. ".format(address) \
                    + "There's likely an issue with iptables or the address and we don't want to break anything by continuing.")
        print(Colors.write("green", "IP tables rules appended, hosts successfully blocked."))

    @classmethod
    def allow(cls, addresses):
        print("Unblocking the following addresses:", ", ".join(addresses))
        for address in addresses:
            cls.callIpTables("-D goregion -s {} -j DROP".format(address))

    @classmethod 
    def reset(cls):
        print("Resetting all goregion rules...")
        print(Colors.write("cyan", "Successfully reset chain.") if cls.callIpTables("-F goregion") == 0 else Colors.write("fail", "Error resetting chain."))


def main():
   #check if iptables chain exists and create it if not
   chainPresent = ipTablesControl.callIpTables("-S | grep -Fx -- '-N goregion' > /dev/null") == 0
   chainBound = ipTablesControl.callIpTables("-S | grep -Fx -- '-A INPUT -j goregion' > /dev/null") == 0
   chainSetup = chainPresent and chainBound
   if not chainSetup:
       print(Colors.write("warning", "\"goregion\" chain not found, attempting to setup..."))
       ipTablesControl.createChain()
       ipTablesControl.bindChain()

   ipTablesControl.reset()

   with urllib.request.urlopen("https://api.steampowered.com/ISteamApps/GetSDRConfig/v1?appid=730") as rawData:
       jsonData = json.loads(rawData.read())
       allPops = jsonData["pops"]
       print(Colors.write("green", "Retrieved SteamDB NetworkDatagramConfig.json version {}.\n".format(jsonData.get("revision"))))

       with open(NETWORK_DIAGRAM_PATH, "r") as networkDiagramData:
           networkDiagramJSON = json.loads(networkDiagramData.read())
           print("The latest available region codes are as follows:")
           validRegions = networkDiagramJSON["regions"].keys()
           validRegionsStr = ", ".join(validRegions).upper()
           print(validRegionsStr)

           selectedRegion = input("Select a region by entering its code: ").lower()
           if selectedRegion not in validRegions:
               print(Colors.write("fail", "You must enter a valid region from the following: " + validRegionsStr))
               exit(1)
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


if args.version:
    print("GoRegion by Skyler Spaeth, v" + __version__ + "\nInitially released on " + __date__)

elif args.ping:
    ipTablesControl.reset()
    print("")
    import pingtable
    pingtable.main()

elif args.reset:
    ipTablesControl.reset()

#default run with no args
else:
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting...")
        exit(1)

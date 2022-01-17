# experimental tests for --ping option later

import urllib.request
import json
import subprocess

class Thresholds:
    MAX_GREEN = 75
    MAX_YELLOW = 150

    @classmethod
    def stylize(cls, value):
        value = int(value)
        if (value <= cls.MAX_GREEN):
            return ("\033[92m{}ms\033[0m".format(value))
        elif (value > cls.MAX_GREEN and value < cls.MAX_YELLOW):
            return ("\033[93m{}ms\033[0m".format(value))
        elif (value >= cls.MAX_YELLOW):
            return ("\033[91m{}ms\033[0m".format(value))

#< is left aligned text, > is right aligned, and ^ is centered
header = f"{'City' : <25}{'IATA' : <10}{'Ping' : <10}"
print(header)
print("-" * len(header))

with urllib.request.urlopen("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json") as rawData:
    jsonData = json.loads(rawData.read())
    allPops = jsonData["pops"]
    
    with open("layout.json", "r") as networkDiagramData:
        networkDiagramJSON = json.loads(networkDiagramData.read())

    def get_pings():
        for (popName, pop) in allPops.items():
            if pop.get("relays") and pop.get("desc"):
                for address in [relay["ipv4"] for relay in pop["relays"]]:
                    try:
                        print("", end=f"\rPinging {pop['desc']}...")
                        command = "/bin/bash -c \"set -o pipefail && ping -c 3 {} | tail -n 1 | awk '{{print \$4}}' | cut -d '/' -f 2 | awk '{{print int(\$1)}}'\"".format(address)
                        response = subprocess.check_output(command, shell=True).strip()
                        print("", end=f"\r{pop['desc'] : <25}{popName.upper() : <10}{Thresholds.stylize(response.decode('ascii')) : <10}\n")
                        break
                    except KeyboardInterrupt:
                        print("\nAborting...")
                        exit(1)
                    except subprocess.CalledProcessError as e:
                        if e.returncode == 1:
                            print("", end=f"\r{pop['desc'] : <25}{popName.upper() : <10}{'Unreachable' : <10}\n")
                        else:
                            raise RuntimeError("Command '{}' returned with nonzero exit code ({}): {}".format(e.cmd, e.returncode, e.output))
    import timeit
    print("Servers pinged in {} seconds.".format(timeit.timeit(get_pings, number=1)))

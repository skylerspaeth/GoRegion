import urllib.request
import json
import subprocess
import timeit
from validate import validate

def main():
    class Thresholds:
        #define thresholds for color coding ping results
        MAX_GREEN = 75
        MAX_YELLOW = 150
        #RED is anything beyond MAX_YELLOW

        @classmethod
        def stylize(cls, value):
            value = int(value)
            if (value <= cls.MAX_GREEN):
                return("\033[92m{}ms\033[0m".format(value))
            elif (value > cls.MAX_GREEN and value < cls.MAX_YELLOW):
                return("\033[93m{}ms\033[0m".format(value))
            elif (value >= cls.MAX_YELLOW):
                return("\033[91m{}ms\033[0m".format(value))

    #< is left aligned text, > is right aligned, and ^ is centered
    header = f"{'City' : <25}{'IATA' : <10}{'Ping' : <10}"
    print(header)
    print("-" * len(header))

    with urllib.request.urlopen("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json") as rawData:
        jsonData = json.loads(rawData.read())
        allPops = jsonData["pops"]
        
        with open("layout.json", "r") as networkDiagramData:
            networkDiagramJSON = json.loads(networkDiagramData.read())

        serversReached = 0
        serversUnreachable = 0
        def getPings():
            for (popName, pop) in allPops.items():
                if pop.get("relays") and pop.get("desc"):
                    addresses = [relay["ipv4"] for relay in pop["relays"]]
                    for addressIdx in range(len(addresses)):
                        try:
                            if validate(addresses[addressIdx]):
                                print("", end=f"\rPinging {popName.upper()} relay {addressIdx + 1} of {len(addresses)}...")
                                packetCount = 1
                                command = "/bin/bash -c \"set -o pipefail && ping -c {} {} | tail -n 1 | awk '{{print \$4}}' | cut -d '/' -f 2 | awk '{{print int(\$1)}}'\"".format(packetCount, addresses[addressIdx])
                                response = subprocess.check_output(command, shell=True).strip()
                                nonlocal serversReached
                                serversReached += 1
                                print("", end=f"\r{pop['desc'] : <25}{popName.upper() : <10}{Thresholds.stylize(response.decode('ascii')) : <10}\n")
                                break
                        except subprocess.CalledProcessError as e:
                            if e.returncode == 1:
                                if (addressIdx + 1 == len(addresses)):
                                    print("", end=f"\r{pop['desc'] : <25}{popName.upper() : <10}{'Unreachable' : <10}\n") 
                                    nonlocal serversUnreachable
                                    serversUnreachable += 1
                            else:
                                raise RuntimeError("Command '{}' returned with nonzero exit code ({}): {}".format(e.cmd, e.returncode, e.output))
                        except KeyboardInterrupt:
                            print("\nAborting...")
                            exit(1)

        pingTime = round(timeit.timeit(getPings, number=1))

        print("")
        if serversUnreachable:
            print("{} server regions pinged in {} seconds, {} of which were unreachable.".format((serversReached + serversUnreachable), pingTime, serversUnreachable))
        else:
            print("{} server regions pinged in {} seconds.".format(serversReached, pingTime))

if __name__ == "__main__":
    main()

#!/bin/bash

# This code isn't meant to be ran, it's just a collection of tests that I will eventually use to calculate the hash for layout.json among other things

#curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r .pops[].desc
#curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r '.pops[] | .relay_addresses'

# Ping average:
ping -c 5 162.254.196.66 | tail -n 1 | awk '{print $4}' | cut -d '/' -f 2 | awk '{print int($1)}'

echo "Querying SteamDB for up-to-date listing of matchmaking server addresses..."
HASH=$(curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r ".pops | keys []" | md5sum | cut -c -32)
curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r ".pops | keys []"
echo -e "$HASH\tNetworkDatagramConfig.json"

mmips="https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json"

#sample='[{"name":"foo"},{"name":"bar"}]'
for row in $(curl -s $mmips | jq -r '.pops[] | @base64'); do
    _jq() {
     echo ${row} | base64 --decode | jq -r ${1}
    }
   printf "\n$(_jq '.desc'):\n$(_jq '.relay_addresses[]')\n"
done

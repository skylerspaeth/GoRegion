#!/bin/bash
#curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r .pops[].desc

echo "Querying SteamDB for up-to-date listing of matchmaking server addresses..."
HASH=$(curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r ".pops | keys []" | md5sum | cut -c -32)
curl -s https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json | jq -r ".pops | keys []"
echo -e "$HASH\tNetworkDatagramConfig.json"

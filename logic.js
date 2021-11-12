#!/usr/bin/env node

let airports = require('./airports.json'); 
const https = require('https');
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const { exec } = require('child_process');

function ipTables(operation, list) {
    if (operation === "block") {
        list.forEach((ip) => {
            exec(`sudo iptables -A INPUT -s ${ip} -j DROP`, (error, stdout, stderr) => {
                if (error) { console.log(error) }
                if (stderr) { console.log(stderr) }
                console.log(stdout);
            });
        });
    }
}

let req = https.get("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json", (res) => {
    let data = '', json_data;

    res.on('data', (stream) => { data += stream });
    res.on('end', () => {
        let valveServers = JSON.parse(data).pops

        console.log("The available region codes are:");
        console.log(Object.keys(airports.regions).map((keyName) => keyName).join(", ").toUpperCase(), "\n");
        rl.question("Which one would you like to queue for? ", (response) => {

            selRegion = response.toLowerCase();
            console.log("Servers that are within region", selRegion.toUpperCase());
            let sitesInRegion = airports.regions[selRegion].cities.map((city) => {
                if (city.referrers) { return city.referrers }
                else { return city.airportCode }
            }).flat();
            console.log("Sites in selected region:", sitesInRegion);

            let valveRelayNames = Object.entries(valveServers).map((server) => { return server[0] });
            let valveRelays = Object.entries(valveServers).map((server) => { return server[1] });
            let valveAddresses = []; 
            for (var i = 0; i < valveRelays.length; i++) {
                if (valveRelays[i].relays) {
                    if (sitesInRegion.includes(valveRelayNames[i]) === false) {
                        valveRelays[i].relays.map((relay) => relay.ipv4 ).forEach((ip) => { valveAddresses.push(ip) });
                    }
                }
            }

            ipTables("block", valveAddresses);
            rl.close();

        });

        rl.on("close", () => { process.exit(0) });
    });
});

req.on('error', (e) => { console.log(e.message) });

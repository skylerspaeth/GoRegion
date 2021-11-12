#!/usr/bin/env node

let airports = require('./airports.json'); 
const https = require('https');
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

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
            console.log(airports.regions[selRegion].cities.map((city) => {
                if (city.referrers) { return city.referrers }
                else { return city.airportCode }
            }).flat());

            let valveAddresses = Object.entries(valveServers).map((e) => { return e[1].relays });
            console.log(valveAddresses);

            rl.close();

        });

        rl.on("close", () => { process.exit(0) });
    });
});

req.on('error', (e) => { console.log(e.message) });

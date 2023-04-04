<p align="center">
  <br>
  <img width="50%" src="https://raw.githubusercontent.com/skylerspaeth/goregion/master/doc/logo.png" alt="GoRegion Logo">
</p>
<p align="center">
    <em>A Python app that allows you to select which Valve matchmaking server you queue for in CS:GO on Linux systems</em>
</p>
<p align="center">
    <img src="https://img.shields.io/github/v/release/skylerspaeth/goregion?include_prereleases&color=%2334D058" alt="Test">
    <img src="https://img.shields.io/badge/platform-linux--64%20%7C%20linux--32-%2334D058" alt="Supported OS/Architectures">
    <img src="https://raw.githubusercontent.com/skylerspaeth/goregion/master/doc/python-versions.svg" alt="Supported Python versions">
</p>

---
GoRegion is a collection of Python scripts that allow you to select which Valve matchmaking server you queue for in CS:GO. What sets it apart from other similar programs is how it dynamically fetches server and IP lists from SteamDB, preventing the maintainer from having to add them manually every time Valve changes their addresses. This benefit is ultimately passed on to the end user, who doesn't have to update the app every time this happens.

<img src="https://raw.githubusercontent.com/skylerspaeth/goregion/master/doc/goregion.png" alt="Screenshot of app">

> **Warning**
> Currently, the SteamDatabase tracking repo hasn't been updated with the new Amsterdam relay addresses. This breaks queueing for specific regions with GoRegion, so a temporary workaround is to run the following script:
> ```bash
> #!/bin/bash
> goregion # select jap
> sudo iptables -A goregion -s 155.133.248.34/32 -j DROP
> sudo iptables -A goregion -s 155.133.248.35/32 -j DROP
> sudo iptables -A goregion -s 155.133.248.36/32 -j DROP
> sudo iptables -A goregion -s 155.133.248.37/32 -j DROP
> sudo iptables -A goregion -s 155.133.248.40/32 -j DROP
> sudo iptables -A goregion -s 155.133.248.41/32 -j DROP
> ```
> This properly disables Amsterdam so you can queue other regions without the risk of getting queued for AMS or another EU server via it.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
  - [Requirements](#requirements)
  - [Portable Usage](#portable-usage)
  - [Installation](#installation)
  - [Uninstallation](#uninstallation)
- [Usage](#usage)
- [Further Plans](#further-plans)

## Introduction
The inspiration behind making GoRegion is the state of North American matchmaking in CS:GO. When every other game in the silver bracket is filled either cheaters or smurfs, trying to rank up is discouraging at best. While your mileage may vary, my experience shows that other regions (such as EU and Japan) are far more balanced and reasonable in their rank distributions.

Programatically, the program works as a wrapper for iptables. It first gets the latest matchmaking IPs being [tracked by SteamDB](https://github.com/SteamDatabase/SteamTracking/blob/master/Random/NetworkDatagramConfig.json) to ensure that the calls to iptables use the most up-to-date information from Valve. An iptables chain is created for GoRegion to be able to append block rules to and destroy with ease.

## Setup
### Requirements
As of now, GoRegion only supports Linux-based systems. I haven't tested it extensively on machines other than my own (Debian 10/Buster), but the only requirements, defined by the commands referenced in the code, are as follows:
- Python 3.0 or higher
- `sudo`
  - Must be installed to allow a non-root user to run GoRegion
  - Permissions will be elevated as needed and you can run the program without sudo
- Netfilter `iptables`
- GNU `grep`
  - Presumably alternative implementations of grep may also have the needed flags (`-F` and `-x`)

### Portable Usage
If you have any remotely standard Linux distibution, there is no setup other than cloning (or downloading a ZIP of) the repo and running the code. If you choose to run the program directly (`./goregion.py`), you'll need to first make it executable by typing the following in the repo directory:
```bash
chmod +x goregion.py
```
Then run it with:
```bash
./goregion.py
# OR
python3 goregion.py
```
### Installation
If you'd like to install GoRegion to run it from anywhere, simply run the install script without arguments:
```bash
./install.sh
```
Then from any directory, just run the command:
```bash
goregion
```
### Uninstallation
Assuming you installed using the included install script, simply use the `-u` or `--uninstall` options of the same script. For instance:
```bash
./install.sh -u
# OR
./install.sh --uninstall
```

## Usage
The program without arguments runs in an interactive mode, showing you the available regions. Additionally, the following arguments are available:
```
usage: goregion [-h] [-p] [-r] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -p, --ping     print latency to each region
  -r, --reset    resets goregion's iptables chain, allowing all regions again
  -v, --version  check installed goregion version
```
The `--ping` option will ping each point of presence (PoP) in the network diagram file. It starts with trying just one relay for that PoP, and will continue if a connection can be established, but if the relay is unreachable, it'll continue through that PoP's list of relays to try and get a ping.

<img width="60%" src="https://raw.githubusercontent.com/skylerspaeth/goregion/master/doc/ping.png" alt="--ping option">


## Further Plans
Many features and improvements are in the works for GoRegion. For the full to-do list, see [TODO.md](doc/TODO.md)

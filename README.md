<p align="center">
  <img src="https://raw.githubusercontent.com/skylerspaeth/goregion/master/doc/logo.png" alt="GoRegion Logo">
</p>
<p align="center">
    <em>A Python app that allows you to select which Valve matchmaking server you queue for in CS:GO on Linux systems</em>
</p>
<p align="center">
    <img src="https://img.shields.io/github/v/release/skylerspaeth/goregion?color=%2334D058" alt="Test">
    <img src="https://img.shields.io/badge/platform-linux--64%20%7C%20linux--32-%2334D058" alt="Supported OS/Architectures">
    <img src="http://skylerspaeth.com/assets/goregion/versions.svg" alt="Supported Python versions">
</p>

---
GoRegion is a collection of Python scripts that allow you to select which Valve matchmaking server you queue for in CS:GO. It sticks out among other similar programs by dynamically fetching server and IP information from SteamDB, preventing you from having to update a list manually every time Valve changes their addresses.

<img width="60%" src="https://raw.githubusercontent.com/skylerspaeth/goregion/master/doc/screenshot.png" alt="Screenshot of app">

## Requirements
As of now, GoRegion only supports Linux-based systems. I haven't tested it extensively on machines other than my own (Debian 10, Buster), but the only requirements, defined by the commands referenced in the code, are as follows:
- `iptables`
- Python 3.0 or higher
- `sudo`
  - Must be installed to allow a non-root user to run GoRegion
  - Permissions will be elevated as needed and you can run the program without sudo
- GNU `grep`
  - Presumably alternative implementations of grep, for example what's found in busybox, may also have the needed flags (`-F` and `-x`)
- `sh` or a bash-like shell aliased to `/bin/sh`
  - I can't think if any situation where this wouldn't be present, but adding this to ensure it's an exhaustive list

## Setup
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
Assuming you installed using the included install script, simple use the `-u` or `--uninstall` options of the same script. For instance:
```bash
./install.sh -u
# OR
./install.sh --uninstall
```

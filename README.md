# goregion
GoRegion is a collection of Python scripts that allow you to select which Valve matchmaking server you queue for in CS:GO.
## Requirements
As of now, GoRegion only supports Linux-based systems. I haven't tested it extensively on machines other than my own (Debian 10, Buster), but the only requirements, defined by the commands referenced in the code, are as follows:
- `iptables`
- `sudo`
  - Must be installed to allow a non-root user to run GoRegion
  - Permissions will be elevated as needed and you can run the program without sudo
- GNU `grep`
  - Presumably alternative implementations of grep, for example what's found in busybox, may also have the needed flags (`-F` and `-x`)
- `sh` or a bash-like shell aliased to `/bin/sh`
  - I can't think if any situation where this wouldn't be present, but adding this to ensure it's an exhaustive list

## Setup
### Installation
If you have any remotely standard Linux distibution, there is no setup other than cloning (or downloading a ZIP of) the repo and running the code. If you choose to run the program directly (`./goregion.py`), you'll need to first make it executable by typing the following in the repo directory:
`chmod +x goregion`
### Running
You can either run with `python3 goregion` or `./goregion.py`.

#!/bin/bash -e

goregion_install () {
  echo "Installing GoRegion..."
  (sudo mkdir -p /opt/goregion && sudo cp *.{py,json} /opt/goregion/) &&
  echo -e "\033[92mSuccessfully created and copied files to goregion directory.\033[0m";
  {
    echo "#!/bin/sh"
    echo "cd /opt/goregion/ && python3 goregion.py \$@"
  } | sudo tee /usr/local/bin/goregion > /dev/null &&
  (sudo chmod +x /usr/local/bin/goregion &&
  echo -e "\033[92mSuccessfully wrote goregion \"binary\" to /usr/local/bin.\033[0m";
  exit 0)
}

goregion_uninstall () {
  echo "Uninstalling GoRegion..."
  sudo rm -rf /opt/goregion/ /usr/local/bin/goregion &&
  (echo -e "\033[92mSuccessfully removed goregion \"binary\" and /opt/goregion directory.\033[0m"; exit 0)
}

command -v python3 > /dev/null || (echo -e "\033[91mInstallation aborted due to Python 3 not being installed. \
Please make sure it is installed and accessible via the command \`python3\` and try again.\033[0m"; exit 1)

if [[ -n "$1" ]] && [[ "$1" != @(--uninstall|-u) ]]; then
  echo -e "\033[31mIncorrect options. This script only takes [-u, --uninstall] (to fully remove) or no arguments (to install).\033[0m"; exit 1
elif [[ "$1" == @(--uninstall|-u) ]]; then
  goregion_uninstall
else
  goregion_install
fi

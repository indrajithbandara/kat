#! /bin/bash

bot_cfg_file='disco_config.yaml'
kat_cfg_file='kat_config.json'

py_36="/usr/bin/env python3.6"
dependencies=(disco-py pyyaml)

# Canonicalize file paths to absolute paths
bot_cfg_file=$(readlink -f ${bot_cfg_file})

# Export this cfg file path to env for this script lifetime so the bot can access it.
export kat_cfg_file=$(readlink -f ${kat_cfg_file})

if [[ $(whoami) == "root" ]]; then
    echo -e "\e[0;31mWarning! You are running the bot as root! Probably should think about this first...\e[0m"
    exit 1
fi

function chk_dep() {
    dependency=$1
    printf "\e[0;34m%-60s" "  Checking that ${dependency} is installed..."
    grep -iq ${dependency} <<< $(${py_36} -m pip list --format=legacy)
    if [[ $? == 0 ]]; then
        echo -e "\e[1;4;32mInstalled\e[0;35m $(${py_36} -m pip show ${dependency} | grep -oP '^Version: .*$')\e[0m"
    else
        echo -e "\e[1;4;31mNot Installed\e[0;37m"
        ${py_36} -m pip install --user ${dependency}
        echo -en "\e[0m"

        if [[ $? != 0 ]]; then
            exit_code=$?
            echo "An error has occurred, dependencies are not met."
            echo "Can not continue!!"
            exit ${exit_code}
        else
            chk_dep ${dependency}
        fi
    fi
}

echo -e "\e[1;33mChecking dependencies are met.\e[0m"
for dependency in ${dependencies[@]}; do
    chk_dep ${dependency}
done

echo

# Make sure all configuration files exist.
for f in $(find templates -type f | xargs); do
    name=$(basename ${f})

    echo -en "\e[36m"
    if [ ! -f ${name} ]; then
        cp ${f} ${name} -v
    fi
    echo -en "\e[0m"
done

echo -e "\e[1;33m"
echo "Starting bot."
echo -e "\e[0m"

${py_36} -m disco.cli --config ${bot_cfg_file}
exit $?
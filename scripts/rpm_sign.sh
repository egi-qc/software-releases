#!/bin/bash

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

# Fuction to sign all packages
function sign_pkgs {
    echo "Signing all packages"
    for pkg in `ls $1`
    do
        echo "Signing: ${1}/${pkg}"
        rpmsign --addsign ${1}/${pkg}
    done
}

# Function to verify/check sign of all packages
function verify_sign {
    echo "Verifying signature all packages"
    for pkg in `ls $1`
    do
        echo "Verify/Check: ${1}/${pkg}"
        rpm --checksig ${1}/${pkg}
        if [ $? -ne 0 ]
        then
            exit 1
        fi
    done
}

if [ $# -ne 2 ]
then
    echo "Usage: $0 <package_name_version> (without extension .json) <0|1>"
    echo "0 - signs and verifies the packages before uploading to umd/cmd repository"
    echo "1 - verifies the packages downloaded from umd/cmd repository"
    exit 1
fi

if [ $2 -eq "0" ]
then
    rpm_dir=$1
    sign_pkgs ${rpm_dir}
    verify_sign ${rpm_dir}
elif [ $2 -eq "1" ]
then
    rpm_dir="/tmp/umdcmd/umdrepo_download/"
    verify_sign ${rpm_dir}
else
    exit 1
fi

exit 0

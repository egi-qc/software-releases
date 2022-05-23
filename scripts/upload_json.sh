#!/bin/bash

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

if [ $# -ne 1 ]
then
    echo "Usage: $0 <package_name_version> (without extension .json)"
    exit 1
fi

eval $(grep = ../../repo.conf | sed 's/ *= */=/g')
echo "${fe_ip} ${fe_user} ${fe_json_dir}"

scp ../json/${1}.json ${fe_user}@${fe_ip}:${fe_json_dir}/${1}.json

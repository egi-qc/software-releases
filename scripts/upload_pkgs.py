#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

"""upload packages to nexus oss repositories
"""

import sys
import utils
from config import Config


if __name__ == '__main__':
    if len(sys.argv) not in [2,3]:
        print('Usage:', sys.argv[0], '<package_name_version> (without extension .json) <config_file> (optional)')
        sys.exit(1)

    prod_name = sys.argv[1]
    ev = Config().getconf(sys.argv[1])
    cfpath = None
    if len(sys.argv) in [3]:
        cfpath = sys.argv[2]

    json_data = utils.get_info_json(ev['json_file'])
    utils.upload_pkg(prod_name, cfpath=cfpath)
    sys.exit(0)

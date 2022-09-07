#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

"""json parser of a UMD or CMD release
"""

import os
import sys
import utils
from config import Config

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<product_metadata_file> (relative path from root repo)')
        sys.exit(1)

    ev = Config.getconf(sys.argv[1])

    # Directory containing the json files
    if not os.path.exists(ev['tmp_dir']):
        os.makedirs(ev['tmp_dir'])
    if not os.path.exists(ev['download_dir']):
        os.makedirs(ev['download_dir'])

    # Create a dictionary with packages: URLs
    pkg_dict = utils.create_dict_pkg(ev['json_file'])

    # Write a list of packages to a file
    with open(ev['file_list'], 'w') as f:
        for pkg in pkg_dict:
            f.write("%s\n" % (ev['tmp_dir'] + '/' + pkg))

    sys.exit(0)

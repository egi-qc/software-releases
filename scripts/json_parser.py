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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<package_metadata_file> (relative path from root repo)')
        sys.exit(1)

    package_metadata_file = sys.argv[1]
    prod_name = os.path.splitext(
        os.path.basename(package_metadata_file)
    )[0]

    ev = utils.get_conf(prod_name)

    # Directory containing the json files
    print(prod_name, ev['json_file'])
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

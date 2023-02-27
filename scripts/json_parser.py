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
    if len(sys.argv) < 2:
        print('Usage:', sys.argv[0],
              '<product_metadata_file> (relative path from root repo) <1> optional')
        print('1 - creates a new json file ready for release/publishing, named release.json')
        print('2 - returns release info from the product\'s json file')
        sys.exit(1)

    # print(f'Get product metadata file: {sys.argv[1]}')
    ev = Config().getconf(sys.argv[1])

    if len(sys.argv) == 3:
        # Option to create new json for release/publishing
        (dst_type, dst_version, platform, arch) = utils.get_info_json(ev['json_file'])

        if sys.argv[2] == '1':
            # full uri is repo_uri_path/rel_uripath ->
            # https://nexusrepoegi.a.incd.pt/repository/umd/5/<OPERATING_SYSTEM>/testing/<ARCH>
            rel_uripath = dst_type + '/' + dst_version + '/' + platform + '/' + 'release' + '/' + arch
            uri_path = ev['repo_uri_path'] + '/' + rel_uripath
            new_json = utils.create_json(ev['json_file'], uri_path)
            new_file = ev['tmp_base_dir'] + '/' + 'release.json'
            utils.write_new_json(new_json, new_file)
            sys.exit(0)
        elif sys.argv[2] == '2':
            print(dst_type, dst_version, platform, arch)
            sys.exit(0)


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

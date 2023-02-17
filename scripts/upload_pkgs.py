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
    if len(sys.argv)  not in [3, 4]:
        print('Usage:', sys.argv[0],
              '<package_name_version> (without extension .json) <0|1> <config_file> (optional)')
        print('0 - uploads packages to testing repository')
        print('1 - uploads packages to release repository')
        sys.exit(1)

    prod_name = sys.argv[1]
    ev = Config().getconf(sys.argv[1])
    (dst_type, dst_version, platform, arch) = utils.get_info_json(ev['json_file'])

    # full uri is repo_uri_path/rel_uripath ->
    # https://nexusrepoegi.a.incd.pt/repository/umd/5/<OPERATING_SYSTEM>/testing|release/<ARCH>
    repo = 'testing'
    if sys.argv[2] == '1':
        repo = 'release'

    rel_uripath = dst_type + '/' + dst_version + '/' + platform + '/' + repo + '/' + arch
    full_uri_path = ev['repo_uri_path'] + '/' + rel_uripath
    print(f'Repository URI path {full_uri_path}')
    cfpath = None
    if len(sys.argv) in [4]:
        cfpath = sys.argv[3]

    utils.upload_pkg(prod_name, full_uri_path, cfpath=cfpath)
    sys.exit(0)

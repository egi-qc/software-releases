#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

"""cleanup packages from testing repository in nexus
"""

import sys
import utils
from config import Config


if __name__ == '__main__':
    if len(sys.argv)  not in [2, 3]:
        print('Usage:', sys.argv[0],
              '<package_name_version> (without extension .json) <config_file> (optional)')
        sys.exit(1)

    prod_name = sys.argv[1]
    ev = Config().getconf(sys.argv[1])
    (dst_type, dst_version, platform, arch) = utils.get_info_json(ev['json_file'])

    # full uri is repo_uri_path/rel_uripath ->
    # https://nexusrepoegi.a.incd.pt/repository/umd/5/<OPERATING_SYSTEM>/testing|release/<ARCH>
    repo = 'testing'
    rel_uripath = dst_type + '/' + dst_version + '/' + platform + '/' + repo + '/' + arch
    full_uri_path = ev['repo_uri_path'] + '/' + rel_uripath
    cfpath = None
    if len(sys.argv) in [3]:
        cfpath = sys.argv[2]

    utils.clean_pkg(prod_name, full_uri_path, cfpath=cfpath)
    sys.exit(0)

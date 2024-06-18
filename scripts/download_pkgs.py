#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

"""json parser of a UMD or CMD release, and download packages
"""

import sys
import utils
from config import Config


if __name__ == '__main__':
    if len(sys.argv) not in [3, 4]:
        print('Usage:', sys.argv[0], '<package_name_version> (without extension .json) <0|1>')
        print('0 - downloads from the original external source')
        print('1 - downloads from the EGI UMD/CMD repository')
        sys.exit(1)

    product_metadata_file = sys.argv[1]
    umd_download = sys.argv[2]
    cfpath = None
    if len(sys.argv) in [4]:
        cfpath = sys.argv[3]

    ev = Config().getconf(product_metadata_file, cfpath=cfpath)
    pkg_dict = utils.create_dict_pkg(ev['json_file'])
    download_dir = ev['tmp_dir']
    if umd_download == '1':
        # download_dir = ev['download_dir']
        (dst_type, dst_version, platform, arch) = utils.get_info_json(ev['json_file'])

        # full uri is repo_uri_path/rel_uripath ->
        # https://nexusrepoegi.a.incd.pt/repository/umd/5/<OPERATING_SYSTEM>/testing/<ARCH>
        rel_uripath = dst_type + '/' + dst_version + '/' + platform + '/' + arch + '/' + 'testing'
        for (pkg, url) in pkg_dict.items():
            pkg_dict[pkg] = ev['repo_uri_path'] + '/' + rel_uripath + '/' + pkg

    if not os.path.exists(download_dir):
        pathlib.Path(download_dir).mkdir(parents=True, exist_ok=True)
    utils.download_pkg(pkg_dict, download_dir)
    print(download_dir)
    sys.exit(0)

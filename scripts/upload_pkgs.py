#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
# Contributor: Samuel Bernardo <samuel@lip.pt>
#

"""upload packages to nexus oss repositories
"""
import os
import sys
import utils
from config import Config


if __name__ == '__main__':
    _TESTING_ = 'testing'
    _UPDATES_ = 'updates'
    _BASE_ = 'base'
    if len(sys.argv)  not in [3, 4]:
        print('Usage:', sys.argv[0],
              '<package_name_version> (without extension .json) <0|1> <config_file> (optional)')
        print('0 - uploads packages to testing repository')
        print('1 - uploads packages to release repository')
        sys.exit(1)

    prod_name = sys.argv[1]
    cfpath = None
    if len(sys.argv) in [4]:
        cfpath = sys.argv[3]

    ev = Config().getconf(sys.argv[1], cfpath=cfpath)
    (dst_type, dst_version, platform, arch) = utils.get_info_json(ev['json_file'])

    # full uri is repo_uri_path/rel_uripath ->
    # https://nexusrepoegi.a.incd.pt/repository/umd/5/<OPERATING_SYSTEM>/<ARCH>/<testing|base|updates>/
    repo = _TESTING_
    if sys.argv[2] == '1':
        repo = _UPDATES_
    if sys.argv[2] == '2':
        repo = _BASE_

    rel_uripath = dst_type + '/' + dst_version + '/' + platform + '/' + arch + '/' + repo
    real_uri = ev['repo_uri_path']
    full_uri_path = ev['repo_uri_path'] + '/' + rel_uripath
    print(f'Repository URI path {full_uri_path}')

    if not utils.upload_pkg(prod_name, full_uri_path, ev['repo_admin'], ev['repo_pass']):
        utils.clean_pkg(prod_name, full_uri_path, cfpath=cfpath)
        if not utils.upload_pkg(prod_name, full_uri_path, ev['repo_admin'], ev['repo_pass']):
            sys.exit(1)
    # Clean up packages from the testing repo after successful copy to the production branch
    if repo == _UPDATES_:
        rel_uripath = dst_type + '/' + dst_version + '/' + platform + '/' + arch + '/' + _TESTING_
        full_uri_path = real_uri + '/' + rel_uripath
        print(f'Repository URI path {full_uri_path}')
        utils.clean_pkg(prod_name, full_uri_path, cfpath=cfpath)

    sys.exit(0)

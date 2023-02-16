# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

"""functions utils
"""

import os
import json
import requests
from config import Config

def create_dict_pkg(json_file):
    '''Create a dictionary with package and respective URL
    pkg_dict = {'pkg1': 'http://xxx/pckg1',}
    '''
    pkg_dict = {}
    with open(json_file, 'r') as jsfd:
        json_data = json.load(jsfd)

    # Get all packages
    for package in json_data["target"]:
        # print(package["platform"], package["arch"])
        for url_file in package["rpms"]:
            # print(url_file)
            pkg = url_file.split('/')[-1]
            pkg_dict[pkg] = url_file

    return pkg_dict

def get_info_json(json_file):
    '''Get information from the json file
    '''
    with open(json_file, 'r') as jsfd:
        json_data = json.load(jsfd)

    return json_data

def download_pkg(pkg_dict, tmp_dir):
    '''Downloads package from given URL
    pkg_dict: dictionary with all URLs of packages
    tmp_dir: output dir from download
    '''
    for (pkg, url) in pkg_dict.items():
        req_get = requests.get(url, allow_redirects=True)
        out_file = tmp_dir  + '/' + pkg
        with open(out_file, 'wb') as file:
            file.write(req_get.content)

def upload_pkg(product_metadata_file, cfpath=None):
    '''Upload all packages to nexus oss repo
    '''
    ev = Config().getconf(product_metadata_file, cfpath=cfpath)
    with open(ev['file_list'], 'r') as f:
        for line in f:
            rpm_file = line.rstrip('\n')
            repo_api = ev['repo_uri'] + '/repository/umd/' + os.path.basename(rpm_file)
            data = open(rpm_file, 'rb').read()
            headers = {"Content-Type": "application/binary",}
            upload = requests.put(repo_api,
                                  data=data,
                                  headers=headers,
                                  auth=(ev['repo_admin'], ev['repo_pass']))
            print(line, upload.status_code)

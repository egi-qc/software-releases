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

    dst_type = json_data["distributionType"].lower()
    dst_version = json_data["distributionVersion"].split('.')[0]
    platform = json_data["target"][0]["platform"]
    arch = json_data["target"][0]["arch"]
    print(f'Get information from {json_file}')
    print(f'Dist Type: {dst_type} - Dist Vers: {dst_version} - Platform: {platform} - Arch: {arch}')
    return (dst_type, dst_version, platform, arch)


def create_json(json_file, uri_path):
    '''Create the json file for release/publication'''
    with open(json_file, 'r') as jsfd:
        json_data = json.load(jsfd)

    all_rpms = []
    for package in json_data["target"]:
        # print(package["platform"], package["arch"])
        for url_file in package["rpms"]:
            # print(url_file)
            pkg = url_file.split('/')[-1]
            rpm_uri = uri_path + '/' + pkg
            all_rpms.append(rpm_uri)

    json_data["target"][0]["rpms"] = all_rpms
    return json_data


def write_new_json(new_json, new_file):
    '''Write the new json to release.json'''
    with open(new_file, 'w') as jsfd:
        json.dump(new_json, jsfd)


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

        # print(f'{pkg} downloaded')        


def upload_pkg(prod_metadata, full_uri_path, repo_admin, repo_pass):
    '''Upload all packages to nexus oss repo
    '''
    ev = Config().getconf(prod_metadata)
    with open(ev['file_list'], 'r') as f:
        for line in f:
            rpm_file = line.rstrip('\n')
            repo_api = full_uri_path + '/' + os.path.basename(rpm_file)
            data = open(rpm_file, 'rb').read()
            headers = {"Content-Type": "application/binary",}
            upload = requests.put(repo_api,
                                  data=data,
                                  headers=headers,
                                  auth=(repo_admin, repo_pass))
            if upload.status_code not in [200]:
                print(upload.status_code, upload.reason)
                return False
    return True


# def clean_pkg(prod_metadata, full_uri_path, cfpath=None):
#     '''Delete testing repo
#     '''
#     ev = Config().getconf(prod_metadata, cfpath=cfpath)
#     req_del = requests.delete(full_uri_path, auth=(ev['repo_admin'], ev['repo_pass']))
#     print(full_uri_path, req_del.status_code)

def clean_pkg(prod_metadata, full_uri_path, repo_admin, repo_pass):
    '''Delete testing repo
    '''
    ev = Config().getconf(prod_metadata)
    with open(ev['file_list'], 'r') as f:
        for line in f:
            rpm_file = line.rstrip('\n')
            repo_api = full_uri_path + '/' + os.path.basename(rpm_file)
            req_del = requests.delete(repo_api, auth=(repo_admin, repo_pass))
            print(repo_api, req_del.status_code)

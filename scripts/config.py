# -*- coding: utf-8 -*-
"""Configurations options and treatment/overrinding"""
import os
from configparser import ConfigParser


class Config:
    """Default configuration values for the whole application. Changes
    to these values should be made via a configuration file read via
    Config.init()
    """
    conf = {}
    conf['repo_uri'] = 'https://mynexusrepo.mydomain'
    conf['repo_admin'] = 'admin'
    conf['repo_pass'] = 'mypass'
    conf['tmp_base_dir'] = '/tmp/umdcmd'
    conf['fe_ip'] = '127.0.0.1'
    conf['fe_user'] = 'someuser'
    conf['fe_json_dir'] = '/var/www/html/json_dir'

    conf['api_uri'] = conf['repo_uri'] + '/service/rest/v1'
    conf['repo_uri_download'] = conf['repo_uri'] + '/repository/umd'
    conf['json_dir'] = '../json'
    conf['download_dir'] = conf['tmp_base_dir'] + '/umdrepo_download'

    conf['json_file'] = ''
    conf['tmp_dir'] = ''
    conf['file_list'] = ''

    def _conf_file_read(self, cfpath, ignore_keys=None):
        """
        Read config file
        """
        cfnparser = ConfigParser()
        cfnparser.read(cfpath)
        for (key, val) in cfnparser.items('DEFAULT'):
            if ignore_keys and key in ignore_keys:
                continue
            if val is not None:
                Config.conf[key] = val

    def _file_override(self, cfpath=None, ignore_keys=None):
        """
        Override values from config file
        """
        _cfpath = 'repo.conf'
        if cfpath:
            _cfpath = cfpath
        if os.path.exists(_cfpath):
            self._conf_file_read(_cfpath, ignore_keys)

    def _env_override(self):
        """Override config with environment"""
        Config.conf['repo_uri'] = os.getenv("UMD_REPO_URI", Config.conf['repo_uri'])
        Config.conf['repo_admin'] = os.getenv("UMD_REPO_ADMIN", Config.conf['repo_admin'])
        Config.conf['repo_pass'] = os.getenv("UMD_REPO_PASS", Config.conf['repo_pass'])
        Config.conf['tmp_base_dir'] = os.getenv("UMD_TMP_BASE_DIR", Config.conf['tmp_base_dir'])
        Config.conf['fe_ip'] = os.getenv("UMD_FE_IP", Config.conf['fe_ip'])
        Config.conf['fe_user'] = os.getenv("UMD_FE_USER", Config.conf['fe_user'])
        Config.conf['fe_json_dir'] = os.getenv("UMD_FE_JSON_DIR", Config.conf['fe_json_dir'])

    def getconf(self, product_metadata_file, cfpath=None):
        """Return all configuration variables"""
        product_name = os.path.splitext(os.path.basename(product_metadata_file))[0]
        Config.conf['json_file'] = Config.conf['json_dir'] + '/' + product_name + '.json'
        Config.conf['tmp_dir'] = Config.conf['tmp_base_dir'] + '/' + product_name
        Config.conf['file_list'] = Config.conf['tmp_base_dir'] + '/' + product_name + '.lst'
        self._file_override(cfpath=cfpath)         # Override with variables in conf file
        self._env_override()          # Override with variables in environment
        return Config.conf

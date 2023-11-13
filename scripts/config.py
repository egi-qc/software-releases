# -*- coding: utf-8 -*-
"""Configurations options and treatment/overrinding"""
import os
from configparser import ConfigParser
import utils


class Config:
    """Default configuration values for the whole application. Changes
    to these values should be made via a configuration file read via
    Config.init()
    """
    conf = {}

    def __init__(self, yaml_file=None) -> None:
        if yaml_file is None:
            self.conf['repo_uri'] = 'https://mynexusrepo.mydomain'
            self.conf['repo_admin'] = 'admin'
            self.conf['repo_pass'] = 'mypass'
            self.conf['tmp_base_dir'] = '/tmp/umdcmd'
            self.conf['json_dir'] = '../'
            self.conf['json_file'] = ''
            self.conf['tmp_dir'] = ''
            self.conf['file_list'] = ''
        else:
            config = utils.load_config(yaml_file)
            self.conf['repo_uri'] = config.get('repo_uri')
            self.conf['repo_admin'] = config.get('repo_admin')
            self.conf['repo_pass'] = config.get('repo_pass')
            self.conf['tmp_base_dir'] = config.get('tmp_base_dir')
            self.conf['json_dir'] = config.get('json_dir')
            self.conf['json_file'] = config.get('json_file')
            self.conf['tmp_dir'] = config.get('tmp_dir')
            self.conf['file_list'] = config.get('file_list')

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

    def getconf(self, product_metadata_file, cfpath=None):
        """Return all configuration variables"""
        product_name = product_metadata_file
        if product_name.endswith('.json'):
             product_name = product_name.split('.json')[0]

        self._file_override(cfpath=cfpath)         # Override with variables in conf file
        self._env_override()          # Override with variables in environment
        Config.conf['json_file'] = Config.conf['json_dir'] + product_name + '.json'
        Config.conf['tmp_dir'] = Config.conf['tmp_base_dir'] + '/' + product_name
        Config.conf['file_list'] = Config.conf['tmp_base_dir'] + '/' + product_name + '.lst'
        Config.conf['api_uri'] = Config.conf['repo_uri'] + '/service/rest/v1'
        Config.conf['repo_uri_path'] = Config.conf['repo_uri'] + '/repository'
        Config.conf['download_dir'] = Config.conf['tmp_base_dir'] + '/umdrepo_download'
        return Config.conf

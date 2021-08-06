import os

import yaml

from typing import Tuple


class Config:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        with open(os.environ['config-path']) as config_file:
            self._config = yaml.load(config_file, yaml.FullLoader)

        if self.debug:
            os.environ['FLASK_RUN_PORT'] = 'TRUE'

    def db_get_key_string_by_name(self, name: str) -> str:
        return self._config['db']['keys'][name]

    @property
    def debug(self) -> bool:
        return self._config['debug']

    @property
    def server_host(self) -> str:
        """ Web server host """
        return self._config['server']['host']

    @property
    def server_port(self) -> int:
        """ Web server port """
        return int(self._config['server']['port'])

    @property
    def db_host(self) -> str:
        """ Database host """
        return self._config['db']['host']

    @property
    def db_port(self) -> int:
        """ Database port """
        return self._config['db']['port']

    @property
    def db_index(self) -> int:
        return int(self._config['db']['index'])

    @property
    def db_test_index(self) -> int:
        """ Redis database index for test data """
        return int(self._config['db']['test_index'])

    @property
    def db_key_prefix(self) -> str:
        """ Redis database key prefix """
        return self._config['db']['key-prefix']

    @property
    def log_file_path(self) -> str:
        """ Absolute path to service log file """
        return self._config['log']['path']

    @property
    def log_rotation_settings(self) -> Tuple[str, str]:
        """
        Log retention settings.

        Returns:
            - rotation_after - how long single file may use.
            - retention - how long old log files must keeping

        For more information go to loguru module documentation
        """
        rotation_after = self._config['log']['rotation']['after']
        retention = self._config['log']['rotation']['retention']
        return rotation_after, retention

import redis

from abc import ABC
from abc import abstractmethod
from typing import Generator

from vcounter.lib.config import Config
from vcounter.lib.logger import logger


class DataBase(ABC):
    """
    Abstract class of database class
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataBase, cls).__new__(cls)

        return cls.instance

    @abstractmethod
    def domain_register(self, timestamp: int, domain: str) -> bool: ...

    @abstractmethod
    def domain_filter(self, date_from: int, date_to: int) -> Generator[str, None, None]: ...

    @abstractmethod
    def status(self) -> bool: ...

    @abstractmethod
    def flush_test_db(self) -> None: ...


class Redis(DataBase):
    def __init__(self, db_index: int = None):
        """
        Database implementation based on Redis database
        :param db_index: index of Redis database.
        """
        super().__init__()
        self._config = Config()

        if db_index is None:
            self._db_index = self._config.db_index
        else:
            self._db_index = db_index

        self._db = redis.StrictRedis(
            host=self._config.db_host,
            port=self._config.db_port,
            db=self._db_index,
            decode_responses=True)

        self._visits_key_name = self._config.db_get_key_string_by_name('visits')

        logger.debug('Redis database driver initialized')

    def _make_key(self, key: str) -> str:
        """
        Add prefix to key name. Helpful when need to separate one project from the other
        in the same Redis database

        :param key: Redis key name
        :return: Concatenated key and prefix (sets in configuration)
        """
        return '{}-{}'.format(self._config.db_key_prefix, key)

    def domain_register(self, timestamp: int, domain: str) -> bool:
        """
        Save visited domain to database

        :param timestamp: date time when domain was visited
        :param domain: domain name
        :return: operation status as boolean
        """
        key = self._make_key(self._visits_key_name)
        if not self._db.xadd(key, {timestamp: domain}):
            return False

        return True

    def domain_filter(self, date_from: int, date_to: int) -> Generator[str, None, None]:
        """
        Query Redis database to filter domains by visitation date time
        :param date_from: timestamp
        :param date_to: timestamp
        :return: subsequence of domain names
        """
        key = self._make_key(self._visits_key_name)
        data = self._db.xrange(key)

        for _, elem in data:
            timestamp, domain_name = list(elem.items())[0]
            if date_from <= int(timestamp) <= date_to:
                yield domain_name

    def flush_test_db(self) -> None:
        """
        Needs for testing purposes. Delete all data from test database
        :return: Nothing
        """
        if self._db_index != self._config.db_test_index:
            raise ValueError('This is not test database')

        self._db.flushall()

    def status(self) -> bool:
        """
        Shows database health
        :return: check result as boolean
        """
        is_healthy = self._db.ping()

        if is_healthy:
            return True

        return False

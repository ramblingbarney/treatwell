from abc import ABC


class BaseClient(ABC):
    @classmethod
    def get_client(cls):
        return cls()

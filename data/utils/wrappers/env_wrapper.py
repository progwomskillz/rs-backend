import os

from domain.entities.exceptions import NotFoundException


class EnvWrapper():
    def get(self, key):
        try:
            return os.environ[key]
        except KeyError:
            raise NotFoundException(f"{key} not found")

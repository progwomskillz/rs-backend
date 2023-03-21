from abc import ABC, abstractmethod

from domain.entities.exceptions import InvalidRequest


class BaseValidationUtil(ABC):
    @abstractmethod
    def validate(self, value):
        pass

    def _append_error(self, key, error):
        if key not in self.errors:
            self.errors[key] = []
        self.errors[key].append(error)

    def _process_errors(self):
        if not self.errors:
            return
        raise InvalidRequest(self.errors)

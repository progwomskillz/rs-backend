from abc import ABC


class BaseProfile(ABC):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class AdminProfile(BaseProfile):
    pass


class CommunitySocialWorkerProfile(BaseProfile):
    pass


class PublicOfficialProfile(BaseProfile):
    pass

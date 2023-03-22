from abc import ABC


class BaseProfile(ABC):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class AdminProfile(BaseProfile):
    pass


class CommunitySocialWorkerProfile(BaseProfile):
    @staticmethod
    def from_create_user_request(create_user_request):
        return CommunitySocialWorkerProfile(
            create_user_request.first_name,
            create_user_request.last_name
        )


class PublicOfficialProfile(BaseProfile):
    @staticmethod
    def from_create_user_request(create_user_request):
        return PublicOfficialProfile(
            create_user_request.first_name,
            create_user_request.last_name
        )

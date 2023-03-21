from domain.entities.users import (
    AdminProfile,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)


class ProfilesFactory():
    @staticmethod
    def admin():
        return AdminProfile("test_first_name", "test_last_name")

    @staticmethod
    def community_social_worker():
        return CommunitySocialWorkerProfile("test_first_name", "test_last_name")

    @staticmethod
    def public_official():
        return PublicOfficialProfile("test_first_name", "test_last_name")

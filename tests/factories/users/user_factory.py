from application.structure import structure
from domain.entities.users import User
from .profiles_factory import ProfilesFactory


class UserFactory():
    @staticmethod
    def generic(role, profile):
        return User(
            "test_id",
            role,
            "test@example.com",
            structure.bcrypt_wrapper.hash(UserFactory.get_password()),
            [],
            profile
        )

    @staticmethod
    def get_password():
        return "test_password"

    @staticmethod
    def admin():
        return UserFactory.generic("admin", ProfilesFactory.admin())

    @staticmethod
    def community_social_worker():
        return UserFactory.generic(
            "community_social_worker",
            ProfilesFactory.community_social_worker()
        )

    @staticmethod
    def public_official():
        return UserFactory.generic(
            "public_official",
            ProfilesFactory.public_official()
        )

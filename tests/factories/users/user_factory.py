from application.structure import structure
from domain.entities.users import User
from domain.utils import constants
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
        return UserFactory.generic(
            constants.user_roles.admin,
            ProfilesFactory.admin()
        )

    @staticmethod
    def community_social_worker():
        return UserFactory.generic(
            constants.user_roles.community_social_worker,
            ProfilesFactory.community_social_worker()
        )

    @staticmethod
    def public_official():
        return UserFactory.generic(
            constants.user_roles.public_official,
            ProfilesFactory.public_official()
        )

from domain.entities.users import (
    User,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)
from domain.utils import constants


class CreateUserUseCase():
    def __init__(
        self, principal_validation_util, rbac_validation_util,
        create_user_request_validation_util, password_util, users_repository
    ):
        self.principal_validation_util = principal_validation_util
        self.rbac_validation_util = rbac_validation_util
        self.create_user_request_validation_util = create_user_request_validation_util
        self.password_util = password_util
        self.users_repository = users_repository

    def create_user(self, create_user_request):
        self.principal_validation_util.validate(create_user_request.principal)
        self.rbac_validation_util.validate(
            create_user_request.principal.user,
            [constants.user_roles.admin]
        )
        self.create_user_request_validation_util.validate(create_user_request)
        user = User(
            None,
            create_user_request.role,
            create_user_request.email,
            self.password_util.hash(create_user_request.password),
            None,
            self.__create_profile(create_user_request)
        )
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        return user

    def __create_profile(self, create_user_request):
        profile_classes = {
            constants.user_roles.community_social_worker: CommunitySocialWorkerProfile,
            constants.user_roles.public_official: PublicOfficialProfile
        }
        return profile_classes[create_user_request.role]\
            .from_create_user_request(create_user_request)

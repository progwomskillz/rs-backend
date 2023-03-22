import boto3

from data.repositories import UsersRepository
from data.translators.auth import TokensPairTranslator
from data.translators.shared import UploadedFileTranslator
from data.translators.users import (
    AdminProfileTranslator,
    CommunitySocialWorkerProfileTranslator,
    PublicOfficialProfileTranslator,
    UserTranslator
)
from data.utils.wrappers import BcryptWrapper, EnvWrapper, JWTWrapper, S3Wrapper
from domain.use_cases.auth import LoginUseCase, LogoutUseCase, RefreshUseCase
from domain.utils.validation.auth import (
    LoginRequestValidationUtil,
    RefreshRequestValidationUtil
)
from domain.utils.validation.shared import UploadedFileValidationUtil
from domain.utils.validation.validators import (
    EmailFormatValidator,
    ExistsUploadedFileValidator,
    PresenceValidator,
    TypeValidator
)
from domain.utils.validation import (
    PrincipalValidationUtil,
    RBACValidationUtil
)
from domain.utils import constants
from presentation.handlers.auth import (
    LoginHandler,
    LogoutHandler,
    RefreshHandler
)
from presentation.presenters.auth import TokensPairPresenter
from presentation.presenters.shared import UploadedFilePresenter
from presentation.presenters import PagePresenter
from presentation.utils import PrincipalUtil


class Structure():
    @property
    def users_repository(self):
        return UsersRepository(
            self.env_wrapper.get("DB_SCHEME"),
            self.env_wrapper.get("DB_USERNAME"),
            self.env_wrapper.get("DB_PASSWORD"),
            self.env_wrapper.get("DB_HOST"),
            self.env_wrapper.get("DB_PORT"),
            self.env_wrapper.get("DB_NAME"),
            "users",
            self.user_translator
        )

    @property
    def tokens_pair_translator(self):
        return TokensPairTranslator()

    @property
    def admin_profile_translator(self):
        return AdminProfileTranslator()

    @property
    def community_social_worker_profile_translator(self):
        return CommunitySocialWorkerProfileTranslator()

    @property
    def public_official_profile_translator(self):
        return PublicOfficialProfileTranslator()

    @property
    def user_translator(self):
        return UserTranslator(
            self.tokens_pair_translator,
            {
                constants.user_roles.admin: self.admin_profile_translator,
                constants.user_roles.community_social_worker: self.community_social_worker_profile_translator,
                constants.user_roles.public_official: self.public_official_profile_translator
            }
        )

    @property
    def bcrypt_wrapper(self):
        return BcryptWrapper(int(self.env_wrapper.get("BCRYPT_COMPLICITY")))

    @property
    def env_wrapper(self):
        return EnvWrapper()

    @property
    def jwt_wrapper(self):
        return JWTWrapper(
            self.env_wrapper.get("JWT_SECRET"),
            int(self.env_wrapper.get("JWT_ACCESS_TTL")),
            int(self.env_wrapper.get("JWT_REFRESH_TTL"))
        )

    @property
    def login_use_case(self):
        return LoginUseCase(
            self.login_request_validation_util,
            self.users_repository,
            self.bcrypt_wrapper,
            self.jwt_wrapper
        )

    @property
    def logout_use_case(self):
        return LogoutUseCase(
            self.principal_validation_util,
            self.users_repository
        )

    @property
    def refresh_use_case(self):
        return RefreshUseCase(
            self.refresh_request_validation_util,
            self.users_repository,
            self.jwt_wrapper
        )

    @property
    def login_request_validation_util(self):
        return LoginRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator,
            self.email_format_validator
        )

    @property
    def refresh_request_validation_util(self):
        return RefreshRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator
        )

    @property
    def email_format_validator(self):
        return EmailFormatValidator()

    @property
    def presence_validator(self):
        return PresenceValidator()

    @property
    def principal_validation_util(self):
        return PrincipalValidationUtil()

    @property
    def rbac_validation_util(self):
        return RBACValidationUtil()

    @property
    def login_handler(self):
        return LoginHandler(self.login_use_case, self.tokens_pair_presenter)

    @property
    def logout_handler(self):
        return LogoutHandler(
            self.logout_use_case,
            None,
            self.principal_util
        )

    @property
    def refresh_handler(self):
        return RefreshHandler(
            self.refresh_use_case,
            self.tokens_pair_presenter
        )

    @property
    def tokens_pair_presenter(self):
        return TokensPairPresenter()

    @property
    def principal_util(self):
        return PrincipalUtil(
            self.env_wrapper.get("JWT_TYPE"),
            self.jwt_wrapper,
            self.users_repository
        )

    @property
    def string_type_validator(self):
        return TypeValidator(str, "string")


structure = Structure()

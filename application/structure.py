from data.repositories import PollsRepository, UsersRepository
from data.translators.auth import TokensPairTranslator
from data.translators.polls import (
    FeedbackTranslator,
    PollTranslator,
    StatsTranslator
)
from data.translators.users import (
    AdminProfileTranslator,
    CommunitySocialWorkerProfileTranslator,
    PublicOfficialProfileTranslator,
    UserTranslator
)
from data.utils.wrappers import BcryptWrapper, EnvWrapper, JWTWrapper
from domain.use_cases.auth import LoginUseCase, LogoutUseCase, RefreshUseCase
from domain.use_cases.polls import (
    CreatePollUseCase,
    GetPollsPageUseCase,
    GetPollsSummaryUseCase
)
from domain.use_cases.users import CreateUserUseCase, GetUsersPageUseCase
from domain.utils.validation.auth import (
    LoginRequestValidationUtil,
    RefreshRequestValidationUtil
)
from domain.utils.validation.polls import (
    CreatePollRequestValidationUtil,
    GetPollsPageRequestValidationUtil
)
from domain.utils.validation.users import (
    CreateUserRequestValidationUtil,
    GetUsersPageRequestValidationUtil
)
from domain.utils.validation.validators import (
    EntryValidator,
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
from presentation.handlers.polls import (
    CreatePollHandler,
    GetPollsPageHandler,
    GetPollsSummaryHandler
)
from presentation.handlers.users import CreateUserHandler, GetUsersPageHandler
from presentation.presenters.auth import TokensPairPresenter
from presentation.presenters.polls import PollPresenter, StatsPresenter
from presentation.presenters.users import (
    AdminProfilePresenter,
    CommunitySocialWorkerProfilePresenter,
    PublicOfficialProfilePresenter,
    UserPresenter
)
from presentation.presenters import ListPresenter, PagePresenter
from presentation.utils import PrincipalUtil


class Structure():
    @property
    def polls_repository(self):
        return PollsRepository(
            self.env_wrapper.get("DB_SCHEME"),
            self.env_wrapper.get("DB_USERNAME"),
            self.env_wrapper.get("DB_PASSWORD"),
            self.env_wrapper.get("DB_HOST"),
            self.env_wrapper.get("DB_PORT"),
            self.env_wrapper.get("DB_NAME"),
            "polls",
            self.poll_translator,
            self.stats_translator
        )

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
    def feedback_translator(self):
        return FeedbackTranslator()

    @property
    def poll_translator(self):
        return PollTranslator(
            self.user_translator,
            self.feedback_translator,
            self.stats_translator
        )

    @property
    def stats_translator(self):
        return StatsTranslator()

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
    def create_poll_use_case(self):
        return CreatePollUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.create_poll_request_validation_util,
            self.polls_repository
        )

    @property
    def get_polls_page_use_case(self):
        return GetPollsPageUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.get_polls_page_request_validation_util,
            self.polls_repository
        )

    @property
    def get_polls_summary_use_case(self):
        return GetPollsSummaryUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.polls_repository
        )

    @property
    def create_user_use_case(self):
        return CreateUserUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.create_user_request_validation_util,
            self.bcrypt_wrapper,
            self.users_repository
        )

    @property
    def get_users_page_use_case(self):
        return GetUsersPageUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.get_users_page_request_validation_util,
            self.users_repository
        )

    @property
    def login_request_validation_util(self):
        return LoginRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator
        )

    @property
    def refresh_request_validation_util(self):
        return RefreshRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator
        )

    @property
    def create_poll_request_validation_util(self):
        return CreatePollRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator,
            self.int_type_validator,
            self.list_type_validator
        )

    @property
    def get_polls_page_request_validation_util(self):
        return GetPollsPageRequestValidationUtil(
            self.presence_validator,
            self.int_type_validator
        )

    @property
    def create_user_request_validation_util(self):
        possible_values = [
            constants.user_roles.community_social_worker,
            constants.user_roles.public_official
        ]
        roles_entry_validator = EntryValidator(
            possible_values,
            f"{possible_values}"
        )
        return CreateUserRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator,
            roles_entry_validator,
            self.users_repository
        )

    @property
    def get_users_page_request_validation_util(self):
        admin_possible_values = [
            constants.user_roles.community_social_worker,
            constants.user_roles.public_official
        ]
        admin_roles_entry_validator = EntryValidator(
            admin_possible_values,
            f"{admin_possible_values}"
        )
        public_official_possible_values = [
            constants.user_roles.community_social_worker
        ]
        public_official_roles_entry_validator = EntryValidator(
            public_official_possible_values,
            f"{public_official_possible_values}"
        )
        roles_entry_validators = {
            constants.user_roles.admin: admin_roles_entry_validator,
            constants.user_roles.public_official: public_official_roles_entry_validator
        }
        return GetUsersPageRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator,
            roles_entry_validators,
            self.int_type_validator
        )

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
    def create_poll_handler(self):
        return CreatePollHandler(
            self.create_poll_use_case,
            self.poll_presenter,
            self.principal_util
        )

    @property
    def get_polls_page_handler(self):
        return GetPollsPageHandler(
            self.get_polls_page_use_case,
            self.polls_page_presenter,
            self.principal_util
        )

    @property
    def get_polls_summary_handler(self):
        return GetPollsSummaryHandler(
            self.get_polls_summary_use_case,
            self.stats_list_presenter,
            self.principal_util
        )

    @property
    def create_user_handler(self):
        return CreateUserHandler(
            self.create_user_use_case,
            self.user_presenter,
            self.principal_util
        )

    @property
    def get_users_page_handler(self):
        return GetUsersPageHandler(
            self.get_users_page_use_case,
            self.users_page_presenter,
            self.principal_util
        )

    @property
    def tokens_pair_presenter(self):
        return TokensPairPresenter()

    @property
    def poll_presenter(self):
        return PollPresenter(self.stats_list_presenter)

    @property
    def polls_page_presenter(self):
        return PagePresenter(self.poll_presenter)

    @property
    def stats_presenter(self):
        return StatsPresenter()

    @property
    def stats_list_presenter(self):
        return ListPresenter(self.stats_presenter)

    @property
    def admin_profile_presenter(self):
        return AdminProfilePresenter()

    @property
    def community_social_worker_profile_presenter(self):
        return CommunitySocialWorkerProfilePresenter()

    @property
    def public_official_profile_presenter(self):
        return PublicOfficialProfilePresenter()

    @property
    def user_presenter(self):
        return UserPresenter(
            {
                constants.user_roles.admin: self.admin_profile_presenter,
                constants.user_roles.community_social_worker: self.community_social_worker_profile_presenter,
                constants.user_roles.public_official: self.public_official_profile_presenter
            }
        )

    @property
    def users_page_presenter(self):
        return PagePresenter(self.user_presenter)

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

    @property
    def int_type_validator(self):
        return TypeValidator(int, "integer")

    @property
    def list_type_validator(self):
        return TypeValidator(list, "array")


structure = Structure()

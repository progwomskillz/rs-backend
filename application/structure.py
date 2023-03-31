from data.repositories.mongo import (
    MongoPollsRepository,
    MongoReviseRequestsRepository,
    MongoUsersRepository
)
from data.translators.mongo.auth import MongoTokensPairTranslator
from data.translators.mongo.polls import (
    MongoFeedbackTranslator,
    MongoPollTranslator,
    MongoStatsTranslator
)
from data.translators.mongo.revise_requests import MongoReviseRequestTranslator
from data.translators.mongo.users import (
    MongoAdminProfileTranslator,
    MongoCommunitySocialWorkerProfileTranslator,
    MongoPublicOfficialProfileTranslator,
    MongoUserTranslator
)
from data.utils.wrappers import BcryptWrapper, EnvWrapper, JWTWrapper
from domain.use_cases.auth import LoginUseCase, LogoutUseCase, RefreshUseCase
from domain.use_cases.polls import (
    CreatePollUseCase,
    GetPollsPageUseCase,
    GetPollsSummaryUseCase
)
from domain.use_cases.revise_requests import (
    CreateReviseRequestUseCase,
    GetReviseRequestsPageUseCase
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
from domain.utils.validation.revise_requests import (
    CreateReviseRequestRequestValidationUtil,
    GetReviseRequestsPageRequestValidationUtil
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
from presentation.handlers.revise_requests import (
    CreateReviseRequestHandler,
    GetReviseRequestsPageHandler
)
from presentation.handlers.users import CreateUserHandler, GetUsersPageHandler
from presentation.presenters.auth import TokensPairPresenter
from presentation.presenters.polls import PollPresenter, StatsPresenter
from presentation.presenters.revise_requests import ReviseRequestPresenter
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
    def mongo_polls_repository(self):
        return MongoPollsRepository(
            self.env_wrapper.get("DB_MONGO_SCHEME"),
            self.env_wrapper.get("DB_MONGO_USERNAME"),
            self.env_wrapper.get("DB_MONGO_PASSWORD"),
            self.env_wrapper.get("DB_MONGO_HOST"),
            self.env_wrapper.get("DB_MONGO_PORT"),
            self.env_wrapper.get("DB_MONGO_NAME"),
            "polls",
            self.mongo_poll_translator,
            self.mongo_stats_translator
        )

    @property
    def mongo_revise_requests_repository(self):
        return MongoReviseRequestsRepository(
            self.env_wrapper.get("DB_MONGO_SCHEME"),
            self.env_wrapper.get("DB_MONGO_USERNAME"),
            self.env_wrapper.get("DB_MONGO_PASSWORD"),
            self.env_wrapper.get("DB_MONGO_HOST"),
            self.env_wrapper.get("DB_MONGO_PORT"),
            self.env_wrapper.get("DB_MONGO_NAME"),
            "revise_requests",
            self.mongo_revise_request_translator
        )

    @property
    def mongo_users_repository(self):
        return MongoUsersRepository(
            self.env_wrapper.get("DB_MONGO_SCHEME"),
            self.env_wrapper.get("DB_MONGO_USERNAME"),
            self.env_wrapper.get("DB_MONGO_PASSWORD"),
            self.env_wrapper.get("DB_MONGO_HOST"),
            self.env_wrapper.get("DB_MONGO_PORT"),
            self.env_wrapper.get("DB_MONGO_NAME"),
            "users",
            self.mongo_user_translator
        )

    @property
    def mongo_tokens_pair_translator(self):
        return MongoTokensPairTranslator()

    @property
    def mongo_feedback_translator(self):
        return MongoFeedbackTranslator()

    @property
    def mongo_poll_translator(self):
        return MongoPollTranslator(
            self.mongo_user_translator,
            self.mongo_feedback_translator,
            self.mongo_stats_translator
        )

    @property
    def mongo_stats_translator(self):
        return MongoStatsTranslator()

    @property
    def mongo_revise_request_translator(self):
        return MongoReviseRequestTranslator(
            self.mongo_user_translator,
            self.mongo_poll_translator
        )

    @property
    def mongo_admin_profile_translator(self):
        return MongoAdminProfileTranslator()

    @property
    def mongo_community_social_worker_profile_translator(self):
        return MongoCommunitySocialWorkerProfileTranslator()

    @property
    def mongo_public_official_profile_translator(self):
        return MongoPublicOfficialProfileTranslator()

    @property
    def mongo_user_translator(self):
        return MongoUserTranslator(
            self.mongo_tokens_pair_translator,
            {
                constants.user_roles.admin: self.mongo_admin_profile_translator,
                constants.user_roles.community_social_worker: self.mongo_community_social_worker_profile_translator,
                constants.user_roles.public_official: self.mongo_public_official_profile_translator
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
            self.mongo_users_repository,
            self.bcrypt_wrapper,
            self.jwt_wrapper
        )

    @property
    def logout_use_case(self):
        return LogoutUseCase(
            self.principal_validation_util,
            self.mongo_users_repository
        )

    @property
    def refresh_use_case(self):
        return RefreshUseCase(
            self.refresh_request_validation_util,
            self.mongo_users_repository,
            self.jwt_wrapper
        )

    @property
    def create_poll_use_case(self):
        return CreatePollUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.create_poll_request_validation_util,
            self.mongo_polls_repository
        )

    @property
    def get_polls_page_use_case(self):
        return GetPollsPageUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.get_polls_page_request_validation_util,
            self.mongo_polls_repository
        )

    @property
    def get_polls_summary_use_case(self):
        return GetPollsSummaryUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.mongo_polls_repository
        )

    @property
    def create_revise_request_use_case(self):
        return CreateReviseRequestUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.create_revise_request_request_validation_util,
            self.mongo_revise_requests_repository,
            self.mongo_polls_repository
        )

    @property
    def get_revise_requests_page_use_case(self):
        return GetReviseRequestsPageUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.get_revise_requests_page_request_validation_util,
            self.mongo_revise_requests_repository
        )

    @property
    def create_user_use_case(self):
        return CreateUserUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.create_user_request_validation_util,
            self.bcrypt_wrapper,
            self.mongo_users_repository
        )

    @property
    def get_users_page_use_case(self):
        return GetUsersPageUseCase(
            self.principal_validation_util,
            self.rbac_validation_util,
            self.get_users_page_request_validation_util,
            self.mongo_users_repository
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
    def create_revise_request_request_validation_util(self):
        return CreateReviseRequestRequestValidationUtil(
            self.presence_validator,
            self.string_type_validator
        )

    @property
    def get_revise_requests_page_request_validation_util(self):
        return GetReviseRequestsPageRequestValidationUtil(
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
            self.mongo_users_repository
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
    def create_revise_request_handler(self):
        return CreateReviseRequestHandler(
            self.create_revise_request_use_case,
            self.revise_request_presenter,
            self.principal_util
        )

    @property
    def get_revise_requests_page_handler(self):
        return GetReviseRequestsPageHandler(
            self.get_revise_requests_page_use_case,
            self.revise_requests_page_presenter,
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
    def revise_request_presenter(self):
        return ReviseRequestPresenter(self.poll_presenter)

    @property
    def revise_requests_page_presenter(self):
        return PagePresenter(self.revise_request_presenter)

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
            self.mongo_users_repository
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

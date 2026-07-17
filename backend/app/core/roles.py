from enum import Enum


class UserRole(str, Enum):

    ADMIN = "admin"

    INVESTIGATOR = "investigator"

    ANALYST = "analyst"

    SUPERVISOR = "supervisor"

    POLICY_MAKER = "policy_maker"
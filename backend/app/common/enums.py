from enum import Enum


class SortOrder(str, Enum):
    """Sorting order: Ascending or Descending."""
    ASC = "asc"
    DESC = "desc"


class Gender(str, Enum):
    """Standard gender enum values."""
    MALE = "Male"
    FEMALE = "Female"
    TRANSGENDER = "Transgender"
    PREFER_NOT_TO_SAY = "Prefer Not To Say"


class IdentificationType(str, Enum):
    """Supported identification document types."""
    AADHAAR = "Aadhaar"
    PASSPORT = "Passport"
    DRIVING_LICENSE = "Driving License"
    VOTER_ID = "Voter ID"
    PAN = "PAN"
    OTHER = "Other"


from enum import Enum

class UserType(str, Enum):
    admin = "1"
    regular = "2"
    owner = "3"

class StatementType(str, Enum):
    FromUser = "company"
    FromCompany = "user"

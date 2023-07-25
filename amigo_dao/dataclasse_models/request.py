from typing import TypedDict, Optional
from dataclasses import dataclass, astuple
from datetime import datetime

# Defining Dataclasses to implement custom type annotations for python objects. 

@dataclass
class AddUserDataClass:
    email: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    country_code: str
    phone_number: int
    preferred_country: str
    profile_completion_status: str
    ts_added: datetime
    ts_updated: Optional[datetime]
    ts_deactivated: Optional[datetime]
    is_active: bool
    linkedin_profile: str
    highest_education: str
    years_experience: int
    field_experience: str

@dataclass
class AddFileDataClass:
    uid: int
    file_type: str
    s3_url: str

@dataclass
class AddUserGradesDataClass: 
    uid: int
    exam: str
    score: int
    appeared_on: datetime

@dataclass
class UpdateUserFilesDataClass:
    uid: int
    file_type: str
    s3_urls: str
    file_name: str

@dataclass
class AddUserFilesDataClass:
    uid: int
    file_type: str
    s3_urls: str
    file_name: Optional[str]

@dataclass
class ClientSignUpDataClass:
    email: str
    plaintext_password: str

@dataclass
class UpdateUserInfoDetails:
    highest_education: str
    years_experience: str
    field_experience: str


from typing import TypedDict, Optional
from dataclasses import dataclass, astuple
from datetime import datetime


@dataclass
class FetchUserDetailsByUID:
    uid: int

@dataclass
class FetchUserFilesByFileType:
    uid: int
    file_type: str

@dataclass
class GetUserResponseDataClass:
    uid: int
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
    years_experience: str
    field_experience: str

@dataclass
class GetUserScoreResponseDataClass:
    uid: int
    gre: Optional[int]
    tofel: Optional[int]
    gmat: Optional[int]
    ielts: Optional[int]

@dataclass
class GetUserFilesDataClass: 
    uid: int
    file_type: str
    s3_urls: str

@dataclass 
class GetUserLoginDataClass:
    uid: int
    email: str
    hashed_password: str
    ts_added: datetime
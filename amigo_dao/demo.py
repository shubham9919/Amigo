from dataclasse_models.request import AddUserDataClass, AddUserGradesDataClass, UpdateUserFilesDataClass, AddUserFilesDataClass
from dataclasse_models.response import GetUserResponseDataClass, FetchUserDetailsByUID, FetchUserFilesByFileType

from datetime import datetime
import json

from amigo_features.get_user import GetUserDetails
from amigo_features.add_user import AddUserDetails
from amigo_features.add_user_grades import AddUserGrades
from amigo_features.get_user_grades import GetUserScoreDetails
from amigo_features.update_user_files import UpdateUserFiles
from amigo_features.add_user_files import AddUserFiles
from amigo_features.get_user_files import GetUserFiles

userdata = {
    "email": "schavan@gmailcom",
    "first_name": "shubham",
    "middlename": "Sunil",
    "last_name": "Chavan",
    "country_code": "US",
    "phone_number": 1234565432,
    "preferred_country": "Canada",
    "profile_completion_status": "BASIC_STAGE_1",
    "ts_added": datetime.now(),
    "is_active": True
}

getUserData = { 
    "uid": 2
}

grades = {
    "uid": 2,
    "exam": "gre",
    "score": 320, 
    "appeared_on": datetime.now(),
}

s3_url = {
  "hsc":"s3://visionbox-demo/grade1.jpg",
  "ssc":"s3://visionbox-demo/grade2.jpg"
}

update_user_files = {
    "uid": 2,
    "file_type": "grade_card",
    "s3_urls": "s3://visionbox-demo/predicted_image_137.jpg",
    "file_name": "ptc"
}

add_user_files = {
    "uid": 2,
    "file_type": "grade_card",
    "s3_urls": json.dumps(s3_url)
}

get_user_files = {
    "uid": 1,
    "file_type": "grade_card"
}

user = AddUserDataClass(userdata.get("email"), userdata.get("first_name"), userdata.get("middlename"), userdata.get("last_name"),
                        userdata.get("country_code"), userdata.get("phone_number"), userdata.get(
                            "preferred_country"), userdata.get("profile_completion_status"),
                        userdata.get("ts_added"), None, None, userdata.get("is_active"))

user_grades = AddUserGradesDataClass(grades.get("uid"), grades.get("exam"), grades.get("appeared_on"))

get_score_details = FetchUserDetailsByUID(grades.get("uid"))

update_user_files = UpdateUserFilesDataClass(update_user_files.get("uid"), update_user_files.get("file_type"), update_user_files.get("s3_urls"), update_user_files.get("file_name"))

add_user_files = AddUserFilesDataClass(add_user_files.get("uid"), add_user_files.get("file_type"), add_user_files.get("s3_urls"))

getuf = FetchUserFilesByFileType(get_user_files.get("uid"), get_user_files.get("file_type"))

#### GET USER DETAILS ####
# getuser = FetchUserDetailsByUID(int(getUserData.get("uid")))
# data = GetUserDetails().get_user_details(getuser)
# print(data)

### ADD USER DETAILS ####
# data = AddUserDetails().add_user_details(user)
# print(data["uid"], data["email"], data["profile_completion_status"])

#### ADD USER GRADES ####
add_grades = AddUserGrades().add_user_grades(user_grades)
print(add_grades)

#### GET USER GRADES ####
# res = GetUserScoreDetails().get_user_score_details(get_score_details)
# print(res)

#### ADD USER DOCS ####
# data = AddUserFiles().add_user_files(add_user_files)
# print(data)

#### UPDATE USER DOCS ####
# data = UpdateUserFiles().update_user_files(update_user_files)
# print(data)

#### GET USER DOCS ####
# data: dict = GetUserFiles().get_user_files(getuf)
# print(data)














# json_data = {
#   "hsc":"s3://visionbox-demo/predicted_image_1680135216.jpg",
#   "ssc":"s3://visionbox-demo/predicted_image_1680135216.jpg"
# }


# print(json_data["degree"])
# json_data = json.dumps(json_data) 

# print(json_data[10])
# json_data = json.loads(json_data)
# print(json_data["hsc"])

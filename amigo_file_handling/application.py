import os
import json
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory, session
from flask_bootstrap import Bootstrap
from datetime import datetime

# Dao feature imports
from amigo_dao.amigo_features.add_user import AddUserDetails
from amigo_dao.amigo_features.add_user_grades import AddUserGrades
from amigo_dao.amigo_features.add_user_files import AddUserFiles
from amigo_dao.amigo_features.client_login import SignUpUser
from amigo_dao.amigo_features.update_user_info import UpdateUserInfo

# Dao Dataclass imports
from amigo_dao.dataclasse_models.request import AddUserDataClass, UpdateUserInfoDetails
from amigo_dao.dataclasse_models.request import AddUserGradesDataClass
from amigo_dao.dataclasse_models.request import AddUserFilesDataClass
from amigo_dao.dataclasse_models.request import ClientSignUpDataClass


# Amigo OIDC Imports
from amigo_oidc.services.services import OIDC
from amigo_oidc.identity_providers.google_oidc.services import GoogleOIDC
from amigo_oidc.dataclass_models.models import LoginUser
from amigo_oidc.identity_providers.google_oidc.user import User

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

lang_tests = []
stat_tests = []
uploaded_file_type = []
lang_test_name = []
stat_tests_name = []
lang_res_array = []
stat_res_array = []
uploaded_files = []
uploaded_file_name = []

stat_details_array = []
lang_details_array = []

files_array = []

user_info_data = {}

gpa_data_array = []


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "your_secret_key"
Bootstrap(app)
# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


# # OAuth 2 client setup
# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    # return the basic user info
    return {}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template("user_info.html")


@app.route('/user_info', methods=['POST', 'GET'])
def handle_data():
    print(request.form)
    email = session.get('email')
    first_name = request.form["first_name"]
    middlename = request.form["middle_name"]
    last_name = request.form["last_name"]
    country_code = request.form["country_code"]
    phone_number = request.form["phone_number"]
    preferred_country = request.form["preferred_country"]
    profile_completion_status = "BASIC_STAGE_2"
    ts_updated = datetime.now()
    is_active = True
    session['user_name'] = first_name + ' ' + last_name
    linkedin_profile = request.form["linkedin_profile"]
    user = AddUserDataClass(email, first_name, middlename, last_name, country_code, phone_number,
                            preferred_country, profile_completion_status, None, ts_updated, None, is_active, linkedin_profile, None, None, None)
    res = UpdateUserInfo().update_user_info_after_signup(user)
    print(res)
    return render_template("user_landing.html", data={'name': session['user_name']})


@app.route('/user_home', methods=['POST', 'GET'])
def user_landing():
    return render_template("user_landing.html", data={'name': session['user_name']})


@app.route('/user_grades', methods=['POST', 'GET'])
def user_grades():
    return render_template("user_grades.html", data={'name': session['user_name']})


@app.route('/handle_user_grades', methods=['POST', 'GET'])
def handle_user_grades():
    print('data ghe ========', request.form)
    user_info_data['field_experience'] = request.form['exp_domain']
    user_info_data['years_experience'] = request.form['exp_years']
    if 'highest_education' in user_info_data:
        pass
    else:
        user_info_data['highest_education'] = request.form['level_of_education']

    if request.form['appeared_lang_exam'] == 'Not Appeared':
        lang_selection = True
    else:
        lang_selection = False

    if request.form['appeared_stat_exam'] == 'Not Appeared':
        stat_selection = True
    else:
        stat_selection = False

    data: dict = request.form
    print('data', data)
    if request.method == 'POST':
        if data is not None and 'lang_appeared_on' in data and (data['lang_appeared_on'] != ''):
            file = request.files['file_lang']
            lang_results = {}
            print('path lang', os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename))
            lang_files = AddUserFilesDataClass(session.get(
                'uid'), 'exams', app.config['UPLOAD_FOLDER'] + '/' + file.filename, request.form['appeared_lang_exam'])
            files_array.append(lang_files)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            lang_results['uid'] = session.get('uid')
            lang_results['exam'] = request.form['appeared_lang_exam']
            lang_results['score'] = data['lang_score']
            lang_results['appeared_on'] = data['lang_appeared_on']
            lang_res_array.append(lang_files)
            lang_details_array.append(lang_results)
            print(lang_res_array)
            lang_tests.append(file.filename)
            lang_test_name.append(request.form['appeared_lang_exam'])
            if 'add_more' in request.form:
                print('cascasc', uploaded_file_type)
                return render_template('user_grades.html', add_more=True)
            return render_template('user_grades.html', stat_tests=stat_tests, stat_tests_name=stat_tests_name, lang_tests=lang_tests, lang_test_name=lang_test_name,
                                   uploaded_files=uploaded_files, uploaded_file_name=uploaded_file_name,
                                   data={'name': session['user_name']}, education_level=user_info_data['highest_education'], lang_selection=lang_selection, stat_selection=stat_selection)
        if data is not None and 'stat_appeared_on' in data and (data['stat_appeared_on'] != ''):
            file = request.files['file_stat']
            stat_details = {}
            print('path stat', os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename))
            stat_files = AddUserFilesDataClass(session.get(
                'uid'), 'exams', app.config['UPLOAD_FOLDER'] + '/' + file.filename,  request.form['appeared_stat_exam'])
            files_array.append(stat_files)
            print('file.filename is ', file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            stat_details['uid'] = session.get('uid')
            stat_details['exam'] = request.form['appeared_stat_exam']
            stat_details['score'] = data['stat_score']
            stat_details['appeared_on'] = data['stat_appeared_on']
            stat_res_array.append(stat_files)
            stat_details_array.append(stat_details)
            print(stat_res_array)
            stat_tests.append(file.filename)
            stat_tests_name.append(request.form['appeared_stat_exam'])
            if 'add_more_stat' in request.form:
                print('cascasc', uploaded_file_type)
                return render_template('user_grades.html', add_more_stat=True)
            return render_template('user_grades.html', stat_tests=stat_tests, stat_tests_name=stat_tests_name, lang_tests=lang_tests, lang_test_name=lang_test_name,
                                   uploaded_files=uploaded_files, uploaded_file_name=uploaded_file_name,
                                   data={'name': session['user_name']}, education_level=user_info_data['highest_education'], lang_selection=lang_selection, stat_selection=stat_selection)
        file = request.files['file_education']
        if file:
            # Save the file to the desired location
            gpa_details = {}
            print(request.form, file.filename)
            files = AddUserFilesDataClass(session.get(
                'uid'), 'grade_card', app.config['UPLOAD_FOLDER'] + '/' + file.filename, request.form['education_level'])
            files_array.append(files)
            gpa_details['uid'] = session.get('uid')
            gpa_details['exam'] = request.form['education_level']
            gpa_details['score'] = request.form['gpa']
            gpa_details['appeared_on'] = None
            gpa_data_array.append(gpa_details)
            print(files_array)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            uploaded_files.append(file.filename)
            uploaded_file_name.append(request.form['education_level'])
        if 'upload_more' in request.form:
            print('cascasc', uploaded_file_type)
            return render_template('user_grades.html', upload_more=True)
        else:
            return render_template('user_grades.html', stat_tests=stat_tests, stat_tests_name=stat_tests_name, lang_tests=lang_tests, lang_test_name=lang_test_name,
                                   uploaded_files=uploaded_files, uploaded_file_name=uploaded_file_name, data={'name': session['user_name']}, education_level=user_info_data['highest_education'],
                                   lang_selection=lang_selection, stat_selection=stat_selection)
    return render_template('user_grades.html', upload_more=False,  stat_tests=stat_tests, stat_tests_name=stat_tests_name, lang_tests=lang_tests, lang_test_name=lang_test_name,
                           uploaded_files=uploaded_files, uploaded_file_name=uploaded_file_name, data={'name': session['user_name']}, education_level=user_info_data['highest_education'], lang_selection=lang_selection, stat_selection=stat_selection)


@app.route('/file_upload', methods=['POST', 'GET'])
def file_upload():
    return render_template('file_upload.html')


@app.route('/upload_done', methods=['GET', 'POST'])
def upload_done():
    print('stat_res_array', stat_res_array)
    print('files_array', files_array)
    print('lang_res_array', lang_res_array)

    print('stat_details_array', stat_details_array)
    print('lang_details_array', lang_details_array)

    file = []
    grade_cards = {}
    certs = {}
    exams = {}
    for file in files_array:
        print(file)
        if file.file_type == 'grade_card':
            grade_cards[file.file_name] = file.s3_urls
        elif file.file_type == 'certificate':
            certs[file.file_name] = file.s3_urls
        elif file.file_type == 'exams':
            exams[file.file_name] = file.s3_urls
    print(certs)
    print(grade_cards)
    data = [
        {
            "uid": session.get('uid'),
            "file_type": 'grade_card',
            "s3_urls": json.dumps(grade_cards)
        },
        {
            "uid": session.get('uid'),
            "file_type": 'certificate',
            "s3_urls": json.dumps(certs)
        },
        {
            "uid": session.get('uid'),
            "file_type": 'exams',
            "s3_urls": json.dumps(exams)
        }
    ]
    res = AddUserFiles().add_user_files(data)
    merged_list = stat_details_array + lang_details_array + gpa_data_array
    print("merged_list===================", merged_list)
    user_grades_res = AddUserGrades().add_user_grades(merged_list)
    update_user_info_obj = UpdateUserInfoDetails(
        user_info_data['highest_education'], user_info_data['years_experience'], user_info_data['field_experience'])
    update_user_info_obj_res = UpdateUserInfo(
    ).update_user_info_detials(update_user_info_obj)
    print(update_user_info_obj_res)
    return render_template("user_landing.html", data={'name': session['user_name']})


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('user_login.html')


@app.route("/handle_login_data", methods=['GET', 'POST'])
def handle_login_data():
    print(request.form)
    user = ClientSignUpDataClass(
        request.form['email_id'], request.form['password'])
    user_data = SignUpUser().sign_up_user(user)
    session['uid'] = user_data['uid']
    session['email'] = user_data['email']
    return render_template('user_info.html', data=None)


# def get_google_provider_config():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login_google", methods=['GET', 'POST'])
def google_login():
    identity_provider = 'google'
    redirect_uri = OIDC(identity_provider).initiate_oidc()
    return redirect(redirect_uri)


@app.route("/login_google/callback")
def callback():
    userinfo_response = GoogleOIDC().process_auth_google()
    unique_id = userinfo_response["sub"]
    users_email = userinfo_response["email"]
    picture = userinfo_response["picture"]
    users_name = userinfo_response["given_name"]
    family_name = userinfo_response["family_name"]


    # # Create a user in your db with the information provided
    # # by Google
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )

    # user = ClientSignUpDataClass(
    #     users_email, None)
    # user_data = SignUpUser().sign_up_user(user)
    # print(user_data)
    # uid = user_data['uid']
    # email = user_data['email']
    
    user = User.get(users_email,users_name, family_name)
    if not user:
        user = User.create(users_email, users_name, family_name)
        
    login_user(user)
    # # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    # Send user back to homepage
    return render_template('user_info.html', data=None)


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')

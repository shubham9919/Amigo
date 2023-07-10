import os
import json
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory, session
from flask_bootstrap import Bootstrap
from datetime import datetime
import jsonschema

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

# Amigo Error Handling Imports 
from amigo_error_handling.errors import (
    CustomError,
    handle_error,
    BadRequestError,
    UnsupportedMediaTypeError,
    InternalServerError,
    NotFoundError
    )

from amigo_common.services import AmigoCommonServices

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

@app.errorhandler(CustomError)
@app.errorhandler(NotFoundError)
def handle_custom_error(error):
    return handle_error(error)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    # return the basic user info
    return User.get_by_id(user_id)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template("user_login.html")

@login_required
@app.route('/user_info', methods=['POST', 'GET'])
def handle_data():
    try:
        if current_user.is_authenticated:
            # instantiating AmigoCommonServices class. 
            amigo_common_services_object = AmigoCommonServices()
            # Formatting data to feed into json schema validation procees.
            json_body = amigo_common_services_object.get_json_body(request.form)
            # JSON schema validation 
            is_json_valid = amigo_common_services_object.validate_schema(json_body, 'user/info')
            # proceed only if data validation is successful.
            if is_json_valid:
                form_data = dict(request.form)
                print("session --- ", session)
                print("session email ----", session.get('email') )
                email = session.get('email')
                profile_completion_status = "completed_stage_2"
                ts_updated = datetime.now()
                is_active = True
                session['user_name'] = form_data['first_name'] + ' ' + form_data['last_name']
                user = AddUserDataClass(email, 
                                        form_data['first_name'], 
                                        form_data['middle_name'], 
                                        form_data['last_name'], 
                                        form_data['country_code'],
                                        form_data['phone_number'],
                                        form_data['preferred_country'],
                                        profile_completion_status, 
                                        None, 
                                        ts_updated, 
                                        None, 
                                        is_active, 
                                        form_data['linkedin_profile'], 
                                        None, 
                                        None, 
                                        None)
                update_user_info_after_signup_result = UpdateUserInfo().update_user_info_after_signup(user)
                print(update_user_info_after_signup_result)
                return render_template("user_landing.html", data={'name': session['user_name']})
            else: 
                print('Schema validation failed.')
                raise BadRequestError('schema validation failed') 
        else:
            return("<h1>Hello<h1>") 
    except BadRequestError as e:
        raise e
    except InternalServerError as e: 
        raise e
    except Exception as e:
        print("Error: ", e)
        raise e

@login_required
@app.route('/user_home', methods=['POST', 'GET'])
def user_landing():
    print(current_user.id)
    if current_user.is_authenticated:
        return render_template("user_landing.html", data={'name': session['user_name']})
    else:
        return render_template("user_login.html")

@login_required
@app.route('/user_grades', methods=['POST', 'GET'])
def user_grades():
    if current_user.is_authenticated:
        return render_template("user_grades.html", data={'name': session['user_name']})
    else:
        return render_template("user_login.html")
    
@login_required
@app.route('/handle_user_grades', methods=['POST'])
def handle_user_grades():
    try:
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
        if request.method == 'POST':
            if data is not None and 'lang_appeared_on' in data and (data['lang_appeared_on'] != ''):
                file = request.files['file_lang']
                is_file_allowed = AmigoCommonServices().allowed_file(file.filename)
                if(is_file_allowed):
                    print('path lang', os.path.join(
                        app.config['UPLOAD_FOLDER'], file.filename))
                    lang_files = AddUserFilesDataClass(session.get(
                        'uid'), 'exams', app.config['UPLOAD_FOLDER'] + '/' + file.filename, request.form['appeared_lang_exam'])
                    files_array.append(lang_files)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    lang_results = get_scores_data(request.form, 'lang')
                    lang_res_array.append(lang_files)
                    lang_details_array.append(lang_results)
                    print(lang_res_array)
                    lang_tests.append(file.filename)
                    lang_test_name.append(request.form['appeared_lang_exam'])
                    if 'add_more' in request.form:
                        return render_template('user_grades.html', add_more=True)
                    return render_template('user_grades.html', 
                                        stat_tests=stat_tests, 
                                        stat_tests_name=stat_tests_name, 
                                        lang_tests=lang_tests, 
                                        lang_test_name=lang_test_name,
                                        uploaded_files=uploaded_files, 
                                        uploaded_file_name=uploaded_file_name,
                                        data={'name': session['user_name']}, 
                                        education_level=user_info_data['highest_education'], 
                                        lang_selection=lang_selection, 
                                        stat_selection=stat_selection)
                else: 
                    raise UnsupportedMediaTypeError("File not supported.")
                
            if data is not None and 'stat_appeared_on' in data and (data['stat_appeared_on'] != ''):
                file = request.files['file_stat']
                # stat_details = {}
                is_file_allowed = AmigoCommonServices().allowed_file(file.filename) 
                if is_file_allowed:
                    stat_files = AddUserFilesDataClass(session.get('uid'), 
                                                    'exams', 
                                                    app.config['UPLOAD_FOLDER'] + '/' + file.filename,  
                                                    request.form['appeared_stat_exam'])
                    files_array.append(stat_files)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    stat_details = get_scores_data(request.form, 'stat')
                    stat_res_array.append(stat_files)
                    stat_details_array.append(stat_details)
                    stat_tests.append(file.filename)
                    stat_tests_name.append(request.form['appeared_stat_exam'])
                    if 'add_more_stat' in request.form:
                        return render_template('user_grades.html', add_more_stat=True)
                    return render_template('user_grades.html', 
                                        stat_tests=stat_tests, 
                                        stat_tests_name=stat_tests_name, 
                                        lang_tests=lang_tests, 
                                        lang_test_name=lang_test_name,
                                        uploaded_files=uploaded_files, 
                                        uploaded_file_name=uploaded_file_name,
                                        data={'name': session['user_name']}, 
                                        education_level=user_info_data['highest_education'], 
                                        lang_selection=lang_selection, 
                                        stat_selection=stat_selection)
                else:
                    raise UnsupportedMediaTypeError("File not supported.")
            file = request.files['file_education']
            is_file_allowed = AmigoCommonServices().allowed_file(file.filename)
            if is_file_allowed:
                # Save the file to the desired location
                # gpa_details = {}
                files = AddUserFilesDataClass(session.get('uid'), 
                                            'grade_card', 
                                            app.config['UPLOAD_FOLDER'] + '/' + file.filename, 
                                            request.form['education_level'])
                files_array.append(files)
                gpa_details = get_scores_data(request.form, 'general')
                gpa_data_array.append(gpa_details)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                uploaded_files.append(file.filename)
                uploaded_file_name.append(request.form['education_level'])
            if 'upload_more' in request.form:
                return render_template('user_grades.html', upload_more=True)
            else:
                return render_template('user_grades.html', 
                                    stat_tests=stat_tests, 
                                    stat_tests_name=stat_tests_name, 
                                    lang_tests=lang_tests, 
                                    lang_test_name=lang_test_name,
                                    uploaded_files=uploaded_files, 
                                    uploaded_file_name=uploaded_file_name, 
                                    data={'name': session['user_name']}, 
                                    education_level=user_info_data['highest_education'],
                                    lang_selection=lang_selection, 
                                    stat_selection=stat_selection)
        return render_template('user_grades.html', 
                            upload_more=False,  
                            stat_tests=stat_tests, 
                            stat_tests_name=stat_tests_name, 
                            lang_tests=lang_tests, 
                            lang_test_name=lang_test_name,
                            uploaded_files=uploaded_files, 
                            uploaded_file_name=uploaded_file_name, 
                            data={'name': session['user_name']}, 
                            education_level=user_info_data['highest_education'], 
                            lang_selection=lang_selection, 
                            stat_selection=stat_selection)
    except UnsupportedMediaTypeError as e:
        raise e 
    except Exception as e:
        print("Error: ", e)
        raise e 

login_required
@app.route('/file_upload', methods=['POST', 'GET'])
def file_upload():
    return render_template('file_upload.html')

login_required
@app.route('/upload_done', methods=['GET', 'POST'])
def upload_done():
    try:
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
        add_user_files_response = AddUserFiles().add_user_files(data)
        print(add_user_files_response)
        merged_list = stat_details_array + lang_details_array + gpa_data_array
        add_user_grades_response = AddUserGrades().add_user_grades(merged_list)
        print(add_user_grades_response)
        update_user_info_obj = UpdateUserInfoDetails(
            user_info_data['highest_education'], user_info_data['years_experience'], user_info_data['field_experience'])
        update_user_info_obj_res = UpdateUserInfo(
        ).update_user_info_detials(update_user_info_obj)
        print(update_user_info_obj_res)
        return render_template("user_landing.html", data={'name': session['user_name']})
    except UnsupportedMediaTypeError as e:
        raise e 
    except Exception as e: 
        print("Error", e)
        raise e



@app.route("/login", methods=['GET', 'POST'])
def login():
    # raise NotFoundError("Custom NOt Found occurred", 404)
    return render_template('user_login.html')

login_required
@app.route("/handle_login_data", methods=['GET', 'POST'])
def handle_login_data():
    try:
        json_body = AmigoCommonServices().get_json_body(request.form)
        is_json_valid = AmigoCommonServices().validate_schema(json_body, 'user/login')
        if(is_json_valid):
            user = ClientSignUpDataClass(
                request.form['email_id'], request.form['password'])
            user = User.get(request.form['email_id'],"NA", "NA",  request.form['password'])
            if not user:
                user = User.create(request.form['email_id'], "NA", "NA", request.form['password'])
            
            login_user(user)
            session["email"] = request.form['email_id']
            session["uid"] = current_user.id
            return render_template('user_info.html', data=None)
        else: 
            print('Schema validation failed.')
            raise BadRequestError('schema validation failed')

    except BadRequestError as e:
        raise e


# def get_google_provider_config():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login_google", methods=['GET', 'POST'])
def google_login():
    try:
        identity_provider = 'google'
        redirect_uri = OIDC(identity_provider).initiate_oidc()
        return redirect(redirect_uri)
    except Exception as e:
        print(e)
        raise e 


@app.route("/login_google/callback")
def callback():
    try:
        userinfo_response = GoogleOIDC().process_auth_google()
        unique_id = userinfo_response["sub"]
        users_email = userinfo_response["email"]
        picture = userinfo_response["picture"]
        users_name = userinfo_response["given_name"]
        family_name = userinfo_response["family_name"]
        user = User.get(users_email,users_name, family_name)
        if not user:
            user = User.create(users_email, users_name, family_name)
            
        login_user(user)
        session['email'] = users_email
        session['uid'] = current_user.id
        # # Doesn't exist? Add it to the database.
        # if not User.get(unique_id):
        #     User.create(unique_id, users_name, users_email, picture)

        # Begin user session by logging the user in
        # Send user back to homepage
        return render_template('user_info.html', data=None)
    except Exception as e:
        print(e)
        raise e 

def get_scores_data(data, exam_type):
    try:
        if exam_type == "lang":
            lang_results = {}
            lang_results['uid'] = session.get('uid')
            lang_results['exam'] = data['appeared_lang_exam']
            lang_results['score'] = data['lang_score']
            lang_results['appeared_on'] = data['lang_appeared_on']
            return lang_results
        elif exam_type == "stat":
            stat_details = {}
            stat_details['uid'] = session.get('uid')
            stat_details['exam'] = data['appeared_stat_exam']
            stat_details['score'] = data['stat_score']
            stat_details['appeared_on'] = data['stat_appeared_on']
            return stat_details
        elif exam_type == "general":
            gpa_details = {}
            gpa_details['uid'] = session.get('uid')
            gpa_details['exam'] = data['education_level']
            gpa_details['score'] = data['gpa']
            gpa_details['appeared_on'] = None
            return gpa_details
    except Exception as e:
        print(e)
        raise e


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return render_template("user_login.html")

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')

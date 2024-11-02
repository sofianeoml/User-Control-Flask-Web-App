from function import *
from library import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    session_id = request.cookies.get('session_id')
    if session_id:
        # Redirect to a different page (like the dashboard) if the session_id exists
        return redirect(url_for('home'))  # Change 'dashboard' to your desired endpoint
    else:
        # Redirect to the login page if there is no session_id
        return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
def home():
    return "Welcome to the Dashboard"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()
        if data.get('username') and data.get('first_name') and data.get('last_name') and data.get('password'):

            # Validate username
            if not re.match(username_regex, data.get('username')) or not data.get('username')[0].isalpha():
                error =  "Username must start with a letter and use only lowercase letters or underscores."
                return(jsonify({'success':False,'message':error}))

            # Validate first name
            if not re.match(name_regex, data.get('first_name')):
                error =  "First name must be less than 26 letters."
                return(jsonify({'success':False,'message':error}))

            # Validate last name
            if not re.match(name_regex, data.get('last_name')):
                error = "Last name must be less than 26 letters."
                return(jsonify({'success':False,'message':error}))

            # Validate password
            if not re.match(password_regex, data.get('password')):
                error = "Password must be at least 8 characters long, contain 1 uppercase, 1 number, and 1 special character."
                return(jsonify({'success':False,'message':error}))
            
            # Define the query to search for the element
            query = {"username": str(data.get('username')).lower()}

            # Check if the element exists
            if users.find_one(query):
                return(jsonify({'success':False,'message':'username already taken !'})) 
            else:
                try:
                    data = {
                        'username':str(data.get('username')).lower(),
                        'created_at':str(get_time_now_ms()),
                        'type':'user',
                        'is_banned':False,
                        'first_name':data.get('first_name'),
                        'last_name':data.get('last_name'),
                        'password':str(hash_password(data.get('password'))),
                    }
                    data["_id"] = get_next_sequence_value("user_id")
                    users.insert_one(data)
                    return(jsonify({'success':True,'message':'Registration successful!'}))
                except Exception as message:
                    return(jsonify({'success':False,'message':str(message)}))
            
        else:
            return(jsonify({'success':False,'message':'Make sure that all Your informations are complete.'}))
            
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        if data.get('username') and data.get('password'):
            # Access a database (create it if it doesn't exist)
            db = client["user-control"]
            
            # Access a collection (create it if it doesn't exist)
            users = db["users"]
            
            # Define the query to search for the element
            query = {"username": str(data.get('username')).lower()}

            user = users.find_one(query)
            # Check if the element exists
            if user:
                try:
                    if str(user.get('password')) == str(hash_password(data.get('password'))):
                        user_id = user.get('_id')
                        if sessions.find_one({'user_id':user_id}):
                            sessions.delete_many({'user_id':user_id})
                            created_at = get_time_now_ms()
                            expired_at = get_time_now_ms() + 86400000
                            try:
                                data = {
                                    'user_id':user_id,
                                    'created_at':created_at,
                                    'expired_at':expired_at
                                }
                                data["_id"] = generate_session_id()
                                result = sessions.insert_one(data)
                                response = jsonify({'success':True,'message':'Login Succesfully ...'})
                                response.set_cookie('session_id', data["_id"])  # Set the session_id in the client's cookies
                                return response
                            except Exception as message:
                                return(jsonify({'success':False,'message':str(message)}))
                        else:
                            created_at = get_time_now_ms()
                            expired_at = get_time_now_ms() + 86400000
                            try:
                                data = {
                                    'user_id':user_id,
                                    'created_at':created_at,
                                    'expired_at':expired_at
                                }
                                data["_id"] = generate_session_id()
                                result = sessions.insert_one(data)
                                response = jsonify({'success':True,'message':'Login Succesfully ...'})
                                response.set_cookie('session_id', data["_id"])  # Set the session_id in the client's cookies
                                return response
                            except Exception as message:
                                return(jsonify({'success':False,'message':str(message)}))
                    else:
                        return(jsonify({'success':False,'message':'username or password incorrect'}))
                except Exception as message:
                    return(jsonify({'success':False,'message':str(message)}))
            else:
                return(jsonify({'success':False,'message':'username or password incorrect'}))
        else:
            return(jsonify({'success':False,'message':'Make sure that all Your informations are complete.'}))

@app.route('/static/css/<file>', methods=['GET'])
def return_style(file):
    return send_from_directory('static/css', file)

if __name__ == '__main__':
    app.run(debug=True)
from function import *
from library import *

app = Flask(__name__)

# Replace with your MongoDB connection string
client = pymongo.MongoClient("mongodb://localhost:27017/") 

username_regex = r'^[a-z_]\w*$'
name_regex = r'^[a-zA-Z]{1,25}$'
password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/]).{8,}$'

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
            
            # Access a database (create it if it doesn't exist)
            db = client["user-control"]
            
            # Access a collection (create it if it doesn't exist)
            users = db["users"]
            
            # Define the query to search for the element
            query = {"username": str(data.get('username')).lower()}

            # Check if the element exists
            if users.find_one(query):
                return(jsonify({'success':False,'message':'username already taken !'})) 
            else:
                try:
                    users.insert_one({
                        'username':str(data.get('username')).lower(),
                        'first_name':data.get('first_name'),
                        'last_name':data.get('last_name'),
                        'password':str(hash_password(data.get('password'))),
                    })
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
                        return(jsonify({'success':True,'message':'Login Succesfully ...'}))
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
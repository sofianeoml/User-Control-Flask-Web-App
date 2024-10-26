from function import *
from library import *

app = Flask(__name__)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()
        if data.get('username') and data.get('first_name') and data.get('last_name') and data.get('password'):
            username_regex = r'^[a-z_]\w*$'
            name_regex = r'^[a-zA-Z]{1,25}$'
            password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/]).{8,}$'

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
            
            return(jsonify({'success':True}))
        else:
            return(jsonify({'success':False,'message':'Make sure that all Your informations are complete.'}))
            

@app.route('/static/css/<file>', methods=['GET'])
def return_style(file):
    return send_from_directory('static/css', file)

if __name__ == '__main__':
    app.run(debug=True)
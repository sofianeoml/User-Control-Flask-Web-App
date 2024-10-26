from function import *
from library import *

app = Flask(__name__)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        return jsonify({'success':True})

@app.route('/static/css/<file>', methods=['GET'])
def return_style(file):
    return send_from_directory('static/css', file)

if __name__ == '__main__':
    app.run(debug=True)
import os
import uuid
from flask import *

from werkzeug import secure_filename
from flask_httpauth import HTTPDigestAuth

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'doc', 'png', 'jpg', 'jpeg', 'odf', 'pages'])
loot_dir = 'loot/'

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'ambrosia'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

auth = HTTPDigestAuth()

users = {
    "admin": "admin",
    "coderuth": "Ruthvik7#",
    "amrutha": "ambrosia"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


def rndIDGen(length, s=""):
    s += str(uuid.uuid4())
    return s[0:length].replace('-', '')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
@auth.login_required
def upload(n=""):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))

    return render_template('index.html', s=os.listdir(app.config['UPLOAD_FOLDER']))


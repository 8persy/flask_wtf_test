from flask import Flask
from flask_wtf import CSRFProtect
from flask_session import Session

from views.user import add_user
from models.users import db
# from models.users import create_table

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

app.config['SECRET_KEY'] = 'sdkfjnvjikqaenvfdkjnew;v'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['WTF_CSRF_TIME_LIMIT'] = 300
app.config["SESSION_FILE_DIR"] = "sessions"

Session(app)
CSRFProtect(app)

db.init_app(app)
# create_table(app)

add_user(app, db)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Accounts

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kenya@2030'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)
db.create_all()

#account = db.session.query.filter_by(username='Vin').first()
account = db.session.query(Accounts).filter(Accounts.username=='Vin').first()
#db.session.query.all()
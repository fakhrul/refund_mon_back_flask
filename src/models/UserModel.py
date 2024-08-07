# src/models/UserModel.py
from marshmallow import fields, Schema, INCLUDE
import datetime
from . import db
from ..app import bcrypt
# from .BlogpostModel import BlogpostSchema
from flask_login import UserMixin

class UserModel(UserMixin, db.Model):
    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    phoneno = db.Column(db.String(128), nullable=True)
    organization = db.Column(db.String(), nullable=True)
    role = db.Column(db.String(), nullable=True)



  # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.phoneno = data.get('phoneno')
        self.organization = data.get('organization')
        self.role = data.get('role')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password' and data.get('password') != '': 
                self.password = self.__generate_hash(data.get('password'))
            else:
                setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)
        
    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

class UserSchema(Schema):
    """
    User Schema
    """
    class Meta:
        unknown = INCLUDE
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    phoneno = fields.Str()
    organization = fields.Str()
    role = fields.Str()


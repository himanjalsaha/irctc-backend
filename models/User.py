from utils.db import db
import uuid


user_roles = db.Table('user_roles',
    db.Column('user_id', db.String(400), db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.String(400), db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUIDs are typically 36 chars
    name = db.Column(db.String(50), unique=True)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Consistent UUID type
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    
    roles = db.relationship('Role', secondary=user_roles, backref='users')

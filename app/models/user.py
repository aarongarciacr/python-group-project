from sqlalchemy.sql import func

from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    # createdAt = db.Column(db.DateTime, server_default=db.func.now())
    # updatedAt = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    createdAt = db.Column(db.DateTime, server_default=func.current_timestamp())
    updatedAt = db.Column(db.DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


    carts = db.relationship('Cart', back_populates='user', cascade="all, delete-orphan")
    favorites = db.relationship('Favorite', back_populates='user', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    products = db.relationship("Product", back_populates="owner")


    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.first_name,
            'lastname': self.last_name,
            'email': self.email
        }

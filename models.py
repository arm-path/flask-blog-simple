from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from slugify import slugify

from app import app

db = SQLAlchemy(app)

post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
                    )


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    content = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=datetime.now())
    tags = db.relationship('Tag', secondary=post_tag, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Post id={self.id}:  {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140), unique=True)
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Tag id={self.id}: {self.title}>'


user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(140))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User id={self.id}: {self.email}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(140), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role id={self.id}: {self.email}>'

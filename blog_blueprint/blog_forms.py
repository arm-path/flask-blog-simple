from wtforms import Form, StringField, TextAreaField, SelectMultipleField, validators
from models import Tag


class PostForm(Form):
    title = StringField('Название', [validators.Length(min=3, max=140)])
    content = TextAreaField('Контент', [validators.Length(min=7, max=255)])
    tags = SelectMultipleField('Теги', coerce=int, choices=[(tag.id, tag.title) for tag in Tag.query.all()])


class TagForm(Form):
    title = StringField('Название', [validators.Length(min=3, max=140)])

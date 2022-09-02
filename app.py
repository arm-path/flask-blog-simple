from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_security import SQLAlchemyUserDatastore, Security

from configuration import Configuration
from admin import PostModelView, TagModelView, HomeAdminIndexView
from forms import LoginFormForBlog

# Настройка Flask приложения.
app = Flask(__name__)
app.config.from_object(Configuration)

from models import db, Post, Tag, User, Role

# Настройка Flask-Migrate.
migrate = Migrate(app, db)

# Настройка Flask-Admin.
admin = Admin(app, name='Flask', url="/", template_mode='bootstrap4', index_view=HomeAdminIndexView(name="Главная"))
admin.add_view(PostModelView(Post, db.session))
admin.add_view(TagModelView(Tag, db.session))

# Настройка Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=LoginFormForBlog)

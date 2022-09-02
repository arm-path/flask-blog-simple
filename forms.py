from flask_security.forms import LoginForm, Required, password_required
from flask_security.forms import StringField, PasswordField, BooleanField, SubmitField


class LoginFormForBlog(LoginForm):
    """ Форма авторизации для блога """

    email = StringField("Электронная почта",
                        validators=[Required(message='EMAIL_NOT_PROVIDED')])
    password = PasswordField("Пароль",
                             validators=[password_required])
    remember = BooleanField("Запомнить")
    submit = SubmitField("Войти")

class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:password@localhost/database_name"
    # TODO: database_name - Имя базы данных, root - Пользователь, password - пароль
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret key"
    # Конфигурация Flask-Security
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "solt"
    SECURITY_MSG_USER_DOES_NOT_EXIST = ("Указанный пользователь не существует", "error")
    SECURITY_MSG_INVALID_PASSWORD = ("Не правильно введен пароль", "error")
    SECURITY_MSG_LOGIN = ("Пожалуйста, войдите, чтобы получить доступ к этой странице", "error")

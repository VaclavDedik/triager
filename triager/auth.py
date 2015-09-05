from wtforms.validators import ValidationError
from flask.ext.login import UserMixin

from triager import login_manager, config


class User(UserMixin):
    def __init__(self, username=None):
        self.username = username

    @property
    def id(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    username = user_id

    config.reload()
    user = None
    if config.config.has_section("auth") \
            and config.config.has_option("auth", username):
        user = User(username)

    return user


def validate_password(form, password_field):
    username = form.username.data
    password = password_field.data
    if not username:
        return None

    config.reload()
    if not (config.config.has_section("auth")
            and config.config.has_option("auth", username)
            and config.config.get("auth", username) == password):
        raise ValidationError("Wrong username or password")
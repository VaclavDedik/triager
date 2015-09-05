from wtforms.validators import ValidationError
from flask.ext.login import UserMixin
from flask import flash, redirect, url_for

from triager import login_manager, config
from utils import hash_pwd


class User(UserMixin):
    def __init__(self, username=None):
        self.username = username

    @property
    def id(self):
        return self.username


@login_manager.unauthorized_handler
def unauthorized():
    flash("Unauthorized access. If you want to access the page, log in first.",
          'error')
    return redirect(url_for('login'))


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
            and config.config.get("auth", username) == hash_pwd(password)):
        raise ValidationError("Wrong username or password")

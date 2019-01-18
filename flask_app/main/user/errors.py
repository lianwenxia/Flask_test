from flask import render_template
from . import user


@user.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 权限不正确
@user.app_errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@user.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
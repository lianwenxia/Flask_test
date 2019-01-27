from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort


class BaseModelview(ModelView):

    def getinfo(self):
        return "this is another model"

    def is_accessible(self):
        if current_user.is_anonymous:
            abort(400)
        else:
            return current_user.is_administrator
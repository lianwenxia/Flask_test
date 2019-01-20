from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class BaseModelview(ModelView):

    def getinfo(self):
        return "this is another model"

    def is_accessible(self):
        return current_user.is_administrator
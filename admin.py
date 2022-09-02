from flask import redirect, url_for, request
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super().on_model_change(form, model, is_created)


class PostModelView(BaseModelView, ModelView):
    column_searchable_list = ['title', ]
    column_filters = ['tags', ]
    create_modal = True
    edit_modal = True


class TagModelView(BaseModelView, ModelView):
    column_searchable_list = ['title', ]
    column_editable_list = ['title', ]
    column_filters = ['posts', ]
    create_modal = True
    edit_modal = True


class HomeAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

from flask_babelex import lazy_gettext as _
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    upload_name = StringField(
        _("Name"),
        validators=[DataRequired()],
        render_kw={"placeholder": "jpg, png, jpeg", "class": "form-control"},
    )
    upload_img = FileField(validators=[FileRequired()], render_kw={"class": "mt-3"})

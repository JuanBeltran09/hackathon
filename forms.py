from wtforms import Form
from wtforms.fields import StringField, PasswordField


class sueloForm (Form):
    vereda = StringField('Vereda')
    cultivo = StringField('Cultivo')
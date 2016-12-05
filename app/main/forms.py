from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    location = StringField('What is your location?', validators=[DataRequired()])
    about_me = TextAreaField('Tell something about yourself: ')
    submit = SubmitField('Submit')
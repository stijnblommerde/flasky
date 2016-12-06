from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, \
    ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField()
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        Regexp('^[A-Za-z]*@{1}[A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers dots or '
               'underscores')]),
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('confirm_password', 'Passwords must match.')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired()])
    submit = SubmitField('Register')


    # custom validation starts with validate_ and run as validator
    # this is just an example, because we could use default unique validator
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address already exists')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')


# TODO: old != new & old != confirm
class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[
        DataRequired()])
    new_password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('confirm_password', 'Passwords must match.')])
    confirm_password = PasswordField('Confirm new password', validators=[
        DataRequired()])
    submit = SubmitField('Change password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request password reset')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('confirm_password', 'Passwords must match.')])
    confirm_password = PasswordField('Confirm new password', validators=[
        DataRequired()])
    submit = SubmitField('Change password')


class ChangeEmailRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    new_email = StringField('New email', validators=[DataRequired()])
    submit = SubmitField('Change email')
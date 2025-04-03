from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm


class SignUpForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Length(min=6, max=30)])
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('SignUp')

    @staticmethod
    def validate_username(form):
        for i in form.name.data:
            if i in '0123456789':
                raise ValidationError('number in name')


class UpdateForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Length(min=6, max=30)])
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('SignUp')

    @staticmethod
    def validate_username(username):
        for i in username.data:
            if i in '0123456789':
                raise ValidationError('number in name')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DateForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # Add validators so that date is not in the future or on this current day

class ThemeLetterGridForm(FlaskForm):
    def create_grid_form():
        setattr(ThemeLetterGridForm, "theme", StringField("Theme", validators=[DataRequired()]))
        for i in range(1, 49):
            field_name = f"letter_{i}"
            setattr(ThemeLetterGridForm, field_name, StringField(field_name, validators=[DataRequired()]))
        setattr(ThemeLetterGridForm, "submit", SubmitField("Submit"))
        return ThemeLetterGridForm()
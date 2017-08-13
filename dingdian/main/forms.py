from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_name = StringField('search', validators=[DataRequired()])
    submit = SubmitField('submit')


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    stock = StringField("Stock", validators=[DataRequired()])
    submit = SubmitField("Add Stock")


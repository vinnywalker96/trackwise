from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, CATEGORY, Product


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Save Password')
    submit = SubmitField('Submit')
    
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
        
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
    
    
class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORY, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    add = SubmitField('Add')
    
class OrderForm(FlaskForm):
    product = SelectField("Product", validators=[DataRequired()])
    order_quantity = IntegerField("Quantity", validators=[DataRequired()])
    create_order = SubmitField('Create Order')
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.product.choices = [(product.id, product.name) for product in Product.query.all()]
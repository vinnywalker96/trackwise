"""Forms  Models for the application."""
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, CATEGORY, Product


class LoginForm(FlaskForm):
    """"Class LoginForm is a model for the login form in the application."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Save Password')
    submit = SubmitField('Submit')
    
    
class RegistrationForm(FlaskForm):
    """"Class RegistrationForm is a model for the registration form in the application."""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    
    def validate_username(self, username):
        """validate_username method checks if the username is already in use"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
        
        
    def validate_email(self, email):
        """validate_email method checks if the email is already in use"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
    
    
class ProductForm(FlaskForm):
    """"ProductForm is a model for the product form in the application."""
    name = StringField("Name", validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORY, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    add = SubmitField('Add')

    
class OrderForm(FlaskForm):
    """OrderForm is a model for the order form in the application.
    """
    product = SelectField("Product" ,validators=[DataRequired()])
    order_quantity = IntegerField("Quantity", validators=[DataRequired()])
    created_by = SelectField("Created By",validators=[DataRequired()])
    create_order = SubmitField('Create Order')
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.product.choices = [(product.name) for product in Product.query.all()]
        self.created_by.choices = [(user.username) for user in User.query.all()]
        
        
class DeleteProductForm(FlaskForm):
    """DeleteProductForm is a model for the delete product form in the application."""
    id = SelectField("ID" ,validators=[DataRequired()])
    name = SelectField("Name" ,validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(DeleteProductForm, self).__init__(*args, **kwargs)
        self.name.choices = [(product.name) for product in Product.query.all()]
        self.id.choices = [(product.id) for product in Product.query.all()]
        
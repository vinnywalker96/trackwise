from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import User,Order, Product
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, ProductForm, OrderForm


@app.route('/')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first()
        if user is None :
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dash')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you're registered!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test Post'},
        {'author': user, 'body': 'Test Post'},
    ]
    
    return render_template('user.html', user=user, posts=posts)


@app.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    reg_users = User.query.count()
    all_orders = Order.query.count()
    all_products = Product.query.count()
    order_users = Order.query.all()
    users = User.query.limit(2).all()
    orders_adm = Order.query.limit(2).all()
    products = Product.query.limit(2).all()
    context = {
        "count_users": reg_users,
        "count_orders": all_orders,
        "count_products": all_products,
        "orders": order_users,
        "users": users,
        "products": products,
    }

    return render_template('dash.html' ,title='Dashboard', context=context)


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    products = Product.query.all()
    form = ProductForm()
    if request.method == 'POST'  and form.validate_on_submit():
        
        product = Product(name=form.name.data,
                    quantity=form.quantity.data, 
                    category=form.category.data,
                    description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products'))
    context = {
        "products": products,
        "form": form
    }
    return render_template('products.html',title="Products", context=context )


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    orders = Order.query.all()
    form = OrderForm()
    if request.method == 'POST'  and form.validate_on_submit():
        
        order = Order(product=form.product.data,
                    order_quantity=form.order_quantity.data, 
                    create_order=form.create_order.data)
        order.created_by = current_user
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders'))
    context = {
        "orders": orders,
        "form": form
    }
    return render_template('orders.html',title="Orders", context=context )
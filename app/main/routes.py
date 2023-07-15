from app import  db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from app.models import User,Order, Product, ProductList, productlist_schema, productlists_schema, CATEGORY
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from flask import request, jsonify
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, ProductForm, OrderForm, DeleteProductForm
from app.main import bp

@bp.route('/')
def index():
    return render_template('index.html', title='Home')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dash'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data).first()
        if user is None :
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dash')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form,)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
            username=form.username.data, 
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you're registered!")
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
        
    
    return render_template('user.html', user=user)

@bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', title="users", users=users)


@bp.route('/dash', methods=['GET', 'POST'])
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
        "orders_adm": orders_adm
    }

    return render_template('dash.html' ,title='Dashboard', context=context)


@bp.route('/products', methods=['GET', 'POST'])
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
        flash("Product, succesfully added!")
        return redirect(url_for('main.products'))
    context = {
        "products": products,
        "form": form,
        "category": CATEGORY
    }
    return render_template('products.html',title="Products", context=context )

@bp.route('/Update', methods=['GET', 'POST'])
@login_required
def Update():
  
    if request.method == "POST":
        data = Order.query.get(request.form.get('id'))
          
        data.name = request.form['name']
        data.category = request.form['category']
        data.quantity = request.form['quantity']
        data.description = request.form['description']
        db.session.merge(data)
        db.session.commit()
        flash("Product, succesfully updated!")
        return redirect(url_for('main.orders'))

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
  
    if request.method == "POST":
        data = Product.query.get(request.form.get('id'))
          
        data.name = request.form['name']
        data.category = request.form['category']
        data.quantity = request.form['quantity']
        data.description = request.form['description']
        db.session.merge(data)
        db.session.commit()
        flash("Product, succesfully updated!")
        return redirect(url_for('main.products'))

@bp.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data = db.get_or_404(Product, id)
    db.session.delete(data)
    db.session.commit()
    flash("Product, succesfully deleted!")
    return redirect(url_for('main.products'))

@bp.route('/Delete/<id>/', methods=['GET', 'POST'])
def Delete(id):
    data = db.get_or_404(Order, id)
    db.session.delete(data)
    db.session.commit()
    flash("Order, succesfully deleted!")
    return redirect(url_for('main.orders'))




@bp.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    orders = Order.query.all()
    user = User.query.filter_by().first_or_404()
    form = OrderForm()
    if request.method == 'POST'  and form.validate_on_submit():

        order = Order(product=form.product.data,
                    order_quantity=form.order_quantity.data, 
                    )
        order.set_current_user(form.created_by.data)
        order.set_date(form.date_created.data)
        db.session.add(order)
        db.session.commit()
        flash("Order, succesfully created!")
        return redirect(url_for('main.orders'))
    context = {
        "orders": orders,
        "form": form,
        "user": user
    }
    return render_template('orders.html',title="Orders", context=context)

@bp.route('/product/', methods=['GET','DELETE', 'POST'])
def delete_product():
    form = DeleteProductForm()
    if request.method == "POST":
        product = Product(name=form.name.data,
                          id=form.id.data)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('main.products'))
        
    return render_template('delete_product.html', title="Delete User", form=form)




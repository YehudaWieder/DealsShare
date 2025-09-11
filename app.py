from math import ceil
import os
from threading import Timer
import time
import webbrowser
from flask import Flask, render_template, request, redirect, session, url_for

from routes.admin_routes import delete_user_by_id, edit_user_details, is_user_admin
from routes.auth_routes import insert_new_user, user_login
from routes.product_routes import delete_product_by_id, insert_new_product
from routes.user_routes import delete_profile, edit_profile_details
from database.user_crud import count_users, get_all_users, get_user
from database.product_crud import count_products, count_user_products, get_product, get_products, get_user_products

from config import PRODUCTS_PER_PAGE, SECRET_KEY, DB_PATH

if not os.path.exists(DB_PATH):
    import database.db_setup
    database.db_setup.create_tables()
    
    import database.seed_data
    Timer(0.2, database.seed_data.seed_data).start()
    time.sleep(3)
    

app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['SESSION_PERMANENT'] = False

""" ------------------------
   Products routes
------------------------- """

@app.route('/')
def home():
    """
    Render home page
    """
    msg = request.args.get("message")
    
    user_id = session.get("user_id")
    user = get_user(user_id)
    
    page = int(request.args.get("page", 1))
    offset = (page - 1) * PRODUCTS_PER_PAGE
    
    products = get_products(offset=offset, limit=PRODUCTS_PER_PAGE)
    
    total_count = count_products()
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)
    
    return render_template('home.html', message=msg, products=products, page=page, total_pages=total_pages, user=user)


@app.route('/product/<int:product_id>')
def product(product_id):
    """
    Render a specific product page by product_id
    """
    msg = request.args.get("message")
    
    product = get_product(product_id)

    return render_template('product.html', message=msg, product=product)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """
    Render user's personal edit product page
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")
    
    user = get_user(session.get("user_id"))
    product = get_product(product_id)
    
    if product["user_id"] != session.get("user_id") and user["role"] != "admin":
        return redirect(url_for('home', message="You are not authorized to edit this product"))
    
    if request.method == 'POST':
        form_data = request.form
        file = request.files.get("image")

        result = insert_new_product(form_data, file, user["user_id"], product_id=product_id)
        if result["success"]:
            return redirect(url_for('product', product_id=product_id, message=result["message"]))
        else:
            return render_template('edit_product.html', message=result["message"], product=product)
    
    return render_template('edit_product.html', message=msg, product=product)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """
    Handle form submission to add a new product
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")
    
    if request.method == 'POST':
        form_data = request.form
        file = request.files.get("image")
        user_id = session.get("user_id")

        result = insert_new_product(form_data, file, user_id)
        if result["success"]:
            return redirect(url_for('product', product_id=result["product_id"], message=result["message"]))
        else:
            return render_template('add_product.html', message=result["message"])
    return render_template('add_product.html', message=msg)

""" ------------------------
   Users routes
------------------------- """

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle registration form submission
    """
    if request.method == 'POST':
        result = insert_new_user(request.form)
        
        if result["success"]:
            return redirect(url_for('login', message=result["message"]))
        return render_template('register.html', message=result["message"])
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle login form submission
    """
    msg = request.args.get("message")
    
    if request.method == 'POST':
        result = user_login(request.form)
        
        if result["success"]:
            session["user_id"] = result["user_id"]
            return redirect(url_for('profile', message=result["message"]))
        elif result["message"] == "Incorrect password":
            return render_template('login.html', message=result["message"])
        return render_template('register.html', message=result["message"])
    
    return render_template('login.html', message=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login', message="You have been logged out"))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Render user's personal profile page
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")    
    user_id = session.get("user_id")
    user = get_user(user_id)
    
    page = int(request.args.get("page", 1))
    offset = (page - 1) * PRODUCTS_PER_PAGE
    
    products = get_user_products(offset=offset, limit=PRODUCTS_PER_PAGE, user_id=user_id)
    
    total_count = count_user_products(user_id)
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)
    
    if request.method == 'POST':
        which_form = request.form.get('submit_button')
        
        if which_form == 'delete profile':
            result = delete_profile(request.form)
            if result["success"]:
                session.clear()
                return redirect(url_for('home', message=result["message"]))
            return render_template('profile.html', products=products, message=result["message"], total_pages=total_pages, user=user)
        
        elif which_form == 'delete product':
            result = delete_product_by_id(request.form)
            return render_template('profile.html', message=msg, products=products, page=page, total_pages=total_pages, user=user)
        
    return render_template('profile.html', message=msg, products=products, page=page, total_pages=total_pages, user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
    Render user's personal edit profile page
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_id = session.get("user_id")
    user = get_user(user_id)
    
    if request.method == 'POST':
        result = edit_profile_details(request.form)
        if result["success"]:
            return redirect(url_for('profile', message=result["message"]))
        return render_template('edit_profile.html', message=result["message"], user=user)
    
    return render_template('edit_profile.html', user=user)

""" ------------------------
   Admin routes
------------------------- """

@app.route('/admin')
def admin():
    """
    Render admin dashboard page
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_id = session.get("user_id")
    
    result = is_user_admin(user_id)
    if not result["success"]:
            return redirect(url_for('login', message=result["message"]))
        
    num_users = count_users()
    num_products = count_products()
    num_clicks = ""
    
    return render_template('admin.html', num_users=num_users, num_products=num_products, num_clicks=num_clicks)


@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    Render list of users for admin
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_id = session.get("user_id")
    
    result = is_user_admin(user_id)
    if not result["success"]:
            return redirect(url_for('login', message=result["message"]))
    
    msg = request.args.get("message")
    users = get_all_users()

    if request.method == 'POST':
        result = delete_user_by_id(request.form)
        return redirect(url_for('users', message=result["message"]))
    
    return render_template('users.html', message=msg, users=users)


@app.route('/products')
def products():
    """
    Render list of prodacts for admin
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_id = session.get("user_id")
    
    result = is_user_admin(user_id)
    if not result["success"]:
            return redirect(url_for('login', message=result["message"]))
        
    msg = request.args.get("message")
    
    page = int(request.args.get("page", 1))
    offset = (page - 1) * PRODUCTS_PER_PAGE
    
    products = get_products(offset=offset, limit=PRODUCTS_PER_PAGE)
    
    total_count = count_products()
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)
    
    return render_template('products.html', message=msg, products=products, page=page, total_pages=total_pages)


@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    """
    Render user's personal edit user page
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_id = session.get("user_id")
    
    result = is_user_admin(user_id)
    if not result["success"]:
            return redirect(url_for('login', message=result["message"]))
    
    edited_user_id = request.args.get("user_id")
    edited_user = get_user(edited_user_id)

    if request.method == 'POST':
        result = edit_user_details(request.form)
        if result["success"]:
            return redirect(url_for('users', message=result["message"]))
        return render_template('edit_user.html', message=result["message"], user=edited_user)
    
    return render_template('edit_user.html', user=edited_user)


if __name__ == '__main__':
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000/")

    Timer(0.5, open_browser).start()

    app.run(debug=False)
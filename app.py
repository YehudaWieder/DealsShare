from threading import Timer
import webbrowser
from flask import Flask, render_template, request, redirect, session, url_for

from routes.admin_routes import delete_user_by_id, edit_user_details, is_user_admin
from routes.auth_routes import insert_new_user, user_login
from routes.user_routes import delete_profile, edit_profile_details
from routes.product_routes import insert_new_product
from database.user_crud import count_users, get_all_users, get_user
from database.product_crud import count_products, get_product, get_products

from config import secret_key

app = Flask(__name__)

app.secret_key = secret_key
app.config['SESSION_PERMANENT'] = False

""" ------------------------
   Products routes
------------------------- """

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render home page
    """
    msg = request.args.get("message")
    
    user_id = session.get("user_id")
    user = get_user(user_id)
    
    offset = 0
    if request.method == 'POST':
        offset += 12
    products = get_products(offset)
    
    return render_template('home.html', message=msg, products=products, user=user)


@app.route('/product/<int:product_id>')
def product(product_id):
    """
    Render a specific product page by product_id
    """
    msg = request.args.get("message")
    
    product = get_product(product_id)

    return render_template('product.html', product_id=product_id, message=msg, product=product)


@app.route('/edit_product', methods=['GET', 'POST'])
def edit_product():
    """
    Render user's personal edit product page
    """
    if "user_id" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")
    
    return render_template('edit_product.html', message=msg)


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
            return result["message"]
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

    if request.method == 'POST':
        result = delete_profile(request.form)
        if result["success"]:
            session.clear()
            return redirect(url_for('home', message=result["message"]))
        return render_template('profile.html', message=result["message"], user=user)
    
    return render_template('profile.html', message=msg, user=user)


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
    
    return render_template('products.html')


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
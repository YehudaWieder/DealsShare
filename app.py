from datetime import datetime
from math import ceil
import os
from threading import Timer
import time
import webbrowser
from flask import Flask, render_template, request, redirect, session, url_for

from routes.admin_routes import delete_user_by_id, edit_user_details, is_user_admin
from routes.auth_routes import insert_new_user, user_login
from routes.product_routes import calculate_pagination_data_by_category, calculate_pagination_data_by_user, calculate_pagination_data_favorites, delete_product_by_id, calculate_pagination_data, get_all_favorite_products_with_seller_info, get_product_with_seller_info, get_products_by_category_with_seller_info, get_user_products_with_ratings, insert_new_product, update_product_in_db, get_all_products_with_seller_info
from routes.user_routes import calculate_users_pagination_data, delete_profile, edit_profile_details, get_all_users_with_stats, get_user_with_stats
from database.user_crud import count_users, get_user
from database.product_crud import count_products, delete_old_products, get_product, rate_product, toggle_favorite

from config import PRODUCTS_PER_PAGE, SECRET_KEY, DB_PATH

if not os.path.exists(DB_PATH):
    import database.db_setup
    database.db_setup.create_tables()
    
    # import database.seed_data
    # Timer(0.2, database.seed_data.seed_data).start()
    # time.sleep(3)
    

app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['SESSION_PERMANENT'] = False

current_time = datetime.now()

@app.before_request
def cleanup_old_products():
    """Cleanup old products before each request."""
    delete_old_products()

""" ------------------------
   Products routes
------------------------- """

@app.route('/')
def home():
    """
    Render home page with optional filters (free shipping, search query)
    """
    msg = request.args.get("message")
    
    user_email = session.get("user_email")
    user = get_user(user_email) if user_email else None
    
    free_shipping = request.args.get('free_shipping') == '1'
    search_query = request.args.get('search_query', '').strip()
    
    filters = {}
    if free_shipping:
        filters['free_shipping'] = True
    if search_query:
        filters['search_query'] = search_query
    
    pagination_data = calculate_pagination_data(int(request.args.get("page", 1)), filters=filters)
    
    products = get_all_products_with_seller_info(
        user_email=user_email,
        offset=pagination_data["offset"],
        limit=PRODUCTS_PER_PAGE,
        filters=filters
    )

    return render_template(
        'home.html',
        message=msg,
        products=products,
        pagination_data=pagination_data,
        user=user,
        current_time=current_time
    )


@app.route('/category/<category_name>')
def category(category_name):
    """
    Render products by category page
    """
    user_email = session.get("user_email")
    user = get_user(user_email)

    search_query = request.args.get("search_query", "").strip()
    free_shipping = request.args.get("free_shipping")

    filters = {}
    if free_shipping:
        filters['free_shipping'] = True
    if search_query:
        filters['search_query'] = search_query
        
    pagination_data = calculate_pagination_data_by_category(
        category_name,
        int(request.args.get("page", 1)),
        filters=filters
    )

    products = get_products_by_category_with_seller_info(
        category_name,
        user_email=user_email,
        offset=pagination_data["offset"],
        limit=PRODUCTS_PER_PAGE,
        filters=filters
    )

    return render_template(
        'category.html',
        category_name=category_name,
        products=products,
        pagination_data=pagination_data,
        current_time=current_time,
        user=user
    )


@app.route('/single_product/<int:product_id>')
def single_product(product_id):
    """
    Render a specific product page by product_id
    """
    user_email = session.get("user_email")
    msg = request.args.get("message")
    
    product = get_product_with_seller_info(user_email=user_email, product_id=product_id)

    return render_template('single_product.html', message=msg, product=product, current_time=current_time)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """
    Handle form submission to add a new product
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")
    
    if request.method == 'POST':
        form_data = request.form
        file = request.files.get("image")
        user_email = session.get("user_email")

        result = insert_new_product(form_data, file, user_email)
        if result["success"]:
            return redirect(url_for('single_product', product_id=result["product_id"], message=result["message"]))
        else:
            return render_template('add_product.html', message=result["message"])
    return render_template('add_product.html', message=msg)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """
    Render user's personal edit product page
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")
    
    user = get_user(session.get("user_email"))
    product = get_product(product_id)
    
    if product["seller_email"] != session.get("user_email") and user["role"] != "admin":
        return redirect(url_for('home', message="You are not authorized to edit this product"))
    
    if request.method == 'POST':
        form_data = request.form
        file = request.files.get("image")

        result = update_product_in_db(form_data, file)
        if result["success"]:
            return redirect(url_for('single_product', product_id=product_id, message=result["message"]))
        else:
            return render_template('edit_product.html', message=result["message"], product=product, user=user)
    
    return render_template('edit_product.html', message=msg, product=product, user=user)

@app.route('/rating/<int:product_id>', methods=['POST'])
def rating(product_id):
    """
    Handle rating submission for a product
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session.get("user_email")
    rating = request.form.get('rating')
    
    rate_product(user_email, product_id, rating)
        
    return redirect(url_for('single_product', product_id=product_id))

@app.route('/update_favorite_status/<int:product_id>', methods=['POST'])
def update_favorite_status(product_id):
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session["user_email"]

    toggle_favorite(user_email, product_id)

    previous_page = request.headers.get("Referer", url_for("login"))
    return redirect(previous_page)


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
            session["user_email"] = result["email"]
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
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")    
    
    user_email = session.get("user_email")
    user = get_user_with_stats(user_email)
    
    free_shipping = request.args.get('free_shipping') == '1'
    search_query = request.args.get('search_query', '').strip()
    
    filters = {}
    if free_shipping:
        filters['free_shipping'] = True
    if search_query:
        filters['search_query'] = search_query
    
    pagination_data = calculate_pagination_data_by_user(
        user_email=user_email, 
        page=int(request.args.get("page", 1)), 
        filters=filters
        )
    
    products = get_user_products_with_ratings(
        user_email=user_email, 
        offset=pagination_data["offset"], 
        limit=PRODUCTS_PER_PAGE,
        filters=filters
        )
    
    if request.method == 'POST':
        which_form = request.form.get('submit_button')
        
        if which_form == 'delete profile':
            result = delete_profile(request.form)
            if result["success"]:
                session.clear()
                return redirect(url_for('home', message=result["message"]))
            return render_template(
                'profile.html', 
                products=products, 
                message=result["message"], 
                pagination_data=pagination_data, 
                user=user, 
                current_time=current_time)
        
        elif which_form == 'delete product':
            result = delete_product_by_id(request.form)

            pagination_data = calculate_pagination_data_by_user(
                user_email=user_email, 
                page=int(request.args.get("page", 1)), 
                filters=filters
                )
            
            products = get_user_products_with_ratings(
                user_email=user_email, 
                offset=pagination_data["offset"], 
                limit=PRODUCTS_PER_PAGE, 
                filters=filters
                )
            
            return render_template(
                'profile.html', 
                message=result['message'], 
                products=products, 
                pagination_data=pagination_data, 
                user=user, 
                current_time=current_time
                )
        
    return render_template(
        'profile.html', 
        message=msg, 
        products=products, 
        pagination_data=pagination_data, 
        user=user, 
        current_time=current_time
        )


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
    Render user's personal edit profile page
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session.get("user_email")
    user = get_user(user_email)
    
    if request.method == 'POST':
        result = edit_profile_details(request.form)
        if result["success"]:
            return redirect(url_for('profile', message=result["message"]))
        return render_template('edit_profile.html', message=result["message"], user=user)
    
    return render_template('edit_profile.html', user=user)

@app.route('/favorites')
def favorites():
    """
    Render the user's favorite products page
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    msg = request.args.get("message")
    
    user_email = session.get("user_email")
    user = get_user_with_stats(user_email)
    
    free_shipping = request.args.get('free_shipping') == '1'
    search_query = request.args.get('search_query', '').strip()
    
    filters = {}
    if free_shipping:
        filters['free_shipping'] = True
    if search_query:
        filters['search_query'] = search_query
    
    pagination_data = calculate_pagination_data_favorites(
        user_email=user_email, 
        page=int(request.args.get("page", 1)), 
        filters=filters
        )
    
    products = get_all_favorite_products_with_seller_info(
        user_email=user_email, 
        offset=pagination_data["offset"], 
        limit=PRODUCTS_PER_PAGE,
        filters=filters
        )
    
    return render_template(
        'favorites.html', 
        message=msg, 
        products=products, 
        pagination_data=pagination_data, 
        user=user, 
        current_time=current_time
        )

""" ------------------------
   Admin routes
------------------------- """

@app.route('/admin')
def admin():
    """
    Render admin dashboard page
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session.get("user_email")
    
    result = is_user_admin(user_email)
    # if not result["success"]:
    #         return redirect(url_for('login', message=result["message"]))
        
    num_users = count_users()
    num_products = count_products()
    num_clicks = "---"  # Placeholder for future implementation
    
    return render_template('admin.html', num_users=num_users, num_products=num_products, num_clicks=num_clicks)


@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    Render list of users for admin
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session.get("user_email")
    
    result = is_user_admin(user_email)
# if not result["success"]:
#         return redirect(url_for('login', message=result["message"]))

    msg = request.args.get("message")

    pagination_data = calculate_users_pagination_data(int(request.args.get("page", 1)))
    users = get_all_users_with_stats()

    if request.method == 'POST':
        result = delete_user_by_id(request.form)
        return redirect(url_for('users', message=result["message"]))

    return render_template('users.html', pagination_data=pagination_data, message=msg, users=users)


@app.route('/products', methods=['GET', 'POST'])
def products():
    """
    Render list of prodacts for admin
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session.get("user_email")
    user=get_user(user_email)
    
    result = is_user_admin(user_email)
    # if not result["success"]:
    #         return redirect(url_for('login', message=result["message"]))
        
    msg = request.args.get("message")
    
    free_shipping = request.args.get('free_shipping') == '1'
    search_query = request.args.get('search_query', '').strip()
    
    filters = {}
    if free_shipping:
        filters['free_shipping'] = True
    if search_query:
        filters['search_query'] = search_query
    
    pagination_data = calculate_pagination_data(
        int(request.args.get("page", 1)), 
        filters=filters
        )
    
    products = get_all_products_with_seller_info(
        user_email=user_email, 
        offset=pagination_data["offset"], 
        limit=PRODUCTS_PER_PAGE, filters=filters
        )

    if request.method == 'POST':
        result = delete_product_by_id(request.form)
        return render_template(
            'products.html', 
            message=result["message"], 
            products=products, 
            pagination_data=pagination_data, 
            current_time=current_time, 
            user=user
            )
    
    return render_template(
        'products.html', 
        message=msg, 
        products=products, 
        pagination_data=pagination_data, 
        current_time=current_time, 
        user=user
        )


@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    """
    Render user's personal edit user page
    """
    if "user_email" not in session:
        return redirect(url_for('login', message="Please login first"))
    
    user_email = session.get("user_email")
    user = get_user(user_email)
    
    result = is_user_admin(user_email)
    if not result["success"]:
            return redirect(url_for('login', message=result["message"]))
    
    edited_user_email = request.args.get("email")
    edited_user = get_user(edited_user_email)

    if request.method == 'POST':
        result = edit_user_details(request.form)
        if result["success"]:
            return redirect(url_for('users', message=result["message"]))
        return render_template('edit_user.html', message=result["message"], edited_user=edited_user, user=user)
    
    return render_template('edit_user.html', edited_user=edited_user, user=user)


if __name__ == '__main__':
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000/")

    Timer(0.5, open_browser).start()

    app.run(debug=False)
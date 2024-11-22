from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from wtforms.validators import EqualTo
from products import products
from sanpham import products1

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(150), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='orders')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Trang chủ
@app.route('/')
def index():
    new_product = [product for product in products if product['category'] == 'Product']
    new_arrivals = [product for product in products if product['category'] == 'new_arrivals']
    men_products = [product for product in products if product['category'] == 'men']
    women_products = [product for product in products if product['category'] == 'women']
    return render_template('base.html', new_product=new_product, new_arrivals=new_arrivals, men_products=men_products, women_products=women_products)

# Trang sản phẩm
@app.route('/product')
def product_list():
    new_product = [product for product in products1 if product['category'] == 'new']
    men_products = [product for product in products1 if product['category'] == 'men']
    women_products = [product for product in products1 if product['category'] == 'women']
    kids_products = [product for product in products1 if product['category'] == 'kids']
    return render_template('products.html', new_product=new_product, men_products=men_products, women_products=women_products, kids_products=kids_products)

@app.route('/new')
def new_products():
    new_products = [p for p in products1 if p.get('category') == 'new']
    return render_template('new.html', products1=new_products)

@app.route('/men')
def men_products():
    men_products = [p for p in products1 if p.get('category') == 'men']
    return render_template('men.html', products1=men_products)



# Chi tiết sản phẩm
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((item for item in products1 if item["id"] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product_detail.html', product=product)


# Thêm sản phẩm vào giỏ hàng
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products1 if p['id'] == product_id), None)
    if not product:
        return "Sản phẩm không tồn tại", 404
    
    if 'cart' not in session or not isinstance(session['cart'], list):
        session['cart'] = []

    cart_item = product.copy()
    price_str = cart_item['price'].replace('.', '').replace(',', '')  # Remove formatting
    cart_item['price_value'] = float(price_str)
    session['cart'].append(cart_item)
    session.modified = True
    return redirect(url_for('cart'))

# Trang giỏ hàng
@app.route('/cart')
def cart():
    cart = session.get('cart')
    if cart is None or not isinstance(cart, list):  
        session['cart'] = []  # đảm bảo giỏ hàng trống
        cart = []  # khởi tạo giỏ hàng
    
    valid_cart = [item for item in cart if isinstance(item, dict)]  # lọc các item
    total = sum(item.get('price_value', 0) for item in valid_cart)  # Tính tổng tiền
    
    return render_template('cart.html', cart=valid_cart, total=total)


# Xóa sản phẩm khỏi giỏ hàng
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [p for p in session['cart'] if isinstance(p, dict) and p.get('id') != product_id]
        session.modified = True
    return redirect(url_for('cart'))

# Thanh toán
@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    total = sum(item.get('price_value', 0) for item in cart)
    estimated_delivery_handling = 0  # Miễn phí giao hàng
    return render_template('checkout.html', cart=cart, total=total, estimated_delivery_handling=estimated_delivery_handling)

# Guest Checkout
@app.route('/guest_checkout', methods=['GET', 'POST'])
def guest_checkout():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        payment_method = request.form['payment_method']
    
        # Xử lý thanh toán ở đây (lưu vào cơ sở dữ liệu, gửi email, v.v.)
        flash('Đơn hàng của bạn đã đặt thành công. Hãy kiểm tra email.', 'success')
        return redirect(url_for('index'))
    
    # Tính tổng số tiền từ giỏ hàng trong session
    cart = session.get('cart', [])
    total = sum(item.get('price_value', 0) for item in cart)
    
    return render_template('guest_checkout.html', total=total)

# Member checkout
#@app.route('/member_checkout', methods=['GET', 'POST'])
# @login_required
# def member_checkout():
#     cart = session.get('cart', [])
#     total = sum(item.get('price_value', 0) for item in cart)

#     if request.method == 'POST':
#         payment_method = request.form['payment_method']
#         # Lưu thông tin đơn hàng vào cơ sở dữ liệu
#         new_order = Order(user_id=current_user.id, total_amount=total, payment_method=payment_method)
#         db.session.add(new_order)
#         db.session.commit()

#         flash('Đơn hàng của bạn đã được xử lý và lưu vào lịch sử mua hàng.', 'success')
#         session.pop('cart', None)  # Xóa giỏ hàng sau khi đặt hàng thành công
#         return redirect(url_for('index'))
#     return render_template('member_checkout.html', total=total, user=current_user)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_shop'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'products.json')
ORDERS_FILE = os.path.join(BASE_DIR, 'orders.json')
USERS_FILE = os.path.join(BASE_DIR, 'users.json')  # Файл пользователей

def load_json(filename, default_value):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(default_value, f, ensure_ascii=False, indent=4)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    # Если пользователя нет в сессии (он не вошел), сразу отправляем его на страницу логина
    if 'user' not in session:
        return redirect(url_for('login'))
        
    # Если он вошел, то показываем товары как обычно
    products = load_json(PRODUCTS_FILE, [])
    return render_template('index.html', products=products)

# ================= АВТОРИЗАЦИЯ И РЕГИСТРАЦИЯ =================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password') # Получаем повторный пароль
        
        if not username or not password or not confirm_password:
            flash('Пожалуйста, заполните все поля', 'danger')
            return redirect(url_for('register'))
            
        # ================= ПРОВЕРКА СОВПАДЕНИЯ И СЛОЖНОСТИ =================
        if password != confirm_password:
            flash('Пароли не совпадают!', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Пароль должен быть не короче 6 символов!', 'danger')
            return redirect(url_for('register'))
            
        if password.isdigit():
            flash('Пароль не может состоять только из цифр! Добавьте буквы.', 'danger')
            return redirect(url_for('register'))
            
        if password.isalpha():
            flash('Пароль не может состоять только из букв! Добавьте цифры.', 'danger')
            return redirect(url_for('register'))
        # ===================================================================
            
        users = load_json(USERS_FILE, [])
        
        if any(u['username'].lower() == username.lower() for u in users):
            flash('Пользователь с таким логином уже существует', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password)
        
        new_user = {
            'id': len(users) + 1,
            'username': username,
            'password': hashed_password
        }
        
        users.append(new_user)
        save_json(USERS_FILE, users)
        
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        
        users = load_json(USERS_FILE, [])
        user = next((u for u in users if u['username'].lower() == username.lower()), None)
        
        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'id': user['id'],
                'username': user['username']
            }
            flash(f'Рады видеть вас, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('index'))

# ================= КОРЗИНА И ЗАКАЗЫ =================

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    p_id = str(product_id)
    cart[p_id] = cart.get(p_id, 0) + 1
        
    session['cart'] = cart
    session.modified = True
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_one/<int:product_id>', methods=['POST'])
def remove_one(product_id):
    cart = session.get('cart', {})
    p_id = str(product_id)
    
    if p_id in cart:
        cart[p_id] -= 1
        if cart[p_id] <= 0:
            cart.pop(p_id)
            
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/delete_item/<int:product_id>', methods=['POST'])
def delete_item(product_id):
    cart = session.get('cart', {})
    p_id = str(product_id)
    
    if p_id in cart:
        cart.pop(p_id)
        
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    products = load_json(PRODUCTS_FILE, [])
    cart = session.get('cart', {})
    
    cart_items = []
    total_price = 0
    
    for p_id, quantity in cart.items():
        product = next((p for p in products if str(p['id']) == p_id), None)
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'total': item_total
            })
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        flash('Для оформления заказа необходимо войти в аккаунт.', 'warning')
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        products = load_json(PRODUCTS_FILE, [])
        orders = load_json(ORDERS_FILE, [])
        
        order_items = {}
        total_price = 0
        
        for p_id, quantity in cart.items():
            product = next((p for p in products if str(p['id']) == p_id), None)
            if product:
                order_items[p_id] = quantity
                total_price += product['price'] * quantity
        
        new_order = {
            'id': len(orders) + 1,
            'user_id': session['user']['id'],  # Привязываем заказ к пользователю
            'customer': {'name': name, 'phone': phone, 'address': address},
            'items': order_items,
            'total_price': total_price,
            'status': 'pending'
        }
        
        orders.append(new_order)
        save_json(ORDERS_FILE, orders)
        
        session.pop('cart', None)
        return render_template('checkout.html', success=True)
        
    return render_template('checkout.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)
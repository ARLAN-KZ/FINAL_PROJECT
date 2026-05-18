import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_shop'  # Нужно для работы корзины (сессий)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCTS_FILE = os.path.join(BASE_DIR, 'products.json')
ORDERS_FILE = os.path.join(BASE_DIR, 'orders.json')

def load_json(filename, default_value):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(default_value, f, ensure_ascii=False, indent=4)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Главная страница с товарами
@app.route('/')
def index():
    products = load_json(PRODUCTS_FILE, [])
    print("=== ЗАГРУЖЕННЫЕ ТОВАРЫ ===")  # Добавь эту строку
    print(products)                         # Добавь эту строку
    return render_template('index.html', products=products)

# Добавление товара в корзину
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    # Превращаем id в строку, так как ключи в JSON/сессиях всегда строки
    p_id = str(product_id)
    
    if p_id in cart:
        cart[p_id] += 1
    else:
        cart[p_id] = 1
        
    session['cart'] = cart
    return redirect(url_for('index'))

# Страница корзины
@app.route('/cart')
def cart():
    products = load_json(PRODUCTS_FILE, [])
    cart = session.get('cart', {})
    
    cart_items = []
    total_price = 0
    
    # Сопоставляем ID из корзины с реальными товарами
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

# Очистить корзину
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

# Страница оформления заказа
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        orders = load_json(ORDERS_FILE, [])
        
        # Создаем новый заказ
        new_order = {
            'id': len(orders) + 1,
            'customer': {'name': name, 'phone': phone, 'address': address},
            'items': cart,
            'status': 'pending'
        }
        
        orders.append(new_order)
        save_json(ORDERS_FILE, orders)
        
        # Очищаем корзину после успешного заказа
        session.pop('cart', None)
        
        return render_template('checkout.html', success=True)
        
    return render_template('checkout.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)
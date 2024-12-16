from flask import Flask, request, jsonify
from store_management import Store, Product, User, ReportGenerator

app = Flask(__name__)
store = Store()

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    user = User(username)
    store.add_user(user)
    return jsonify({"message": f"User {username} added successfully!"}), 201


@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    if not all(key in data for key in ("name", "price", "stock")):
        return jsonify({"error": "Missing product data"}), 400
    product = Product(data['name'], data['price'], data['stock'])
    store.add_product(product)
    return jsonify({"message": f"Product {data['name']} added"}), 201

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    if not all(key in data for key in ("username", "product_name", "quantity")):
        return jsonify({"error": "Missing order data"}), 400
    try:
        order = store.create_order(data['username'], data['product_name'], data['quantity'])
        return jsonify({"message": f"Order created for {data['username']}", "order_id": len(store.orders) - 1}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_sales_report', methods=['GET'])
def get_sales_report():
    report = ReportGenerator.generate_sales_report(store)
    return jsonify({"report": report})

# Добавленный маршрут для формы добавления пользователя
@app.route('/add_user_form', methods=['GET'])
def add_user_form():
    return """
    <h1>Add User</h1>
    <form action="/add_user" method="post">
        <input type="text" id="username" name="username" placeholder="Enter username">
        <button type="submit">Submit</button>
    </form>
    """

@app.route('/')
def home():
    return """
    <h1>Welcome to Store Management System</h1>
    <p>Use the API endpoints to manage users, products, and orders.</p>
    <ul>
        <li>POST /add_user</li>
        <li>POST /add_product</li>
        <li>POST /create_order</li>
        <li>GET /get_sales_report</li>
        <li>GET /add_user_form</li>  <!-- Новая форма добавления пользователя -->
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True)

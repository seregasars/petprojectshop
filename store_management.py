# store_management.py

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, amount):
        if self.stock + amount < 0:
            raise ValueError("Not enough stock")
        self.stock += amount

    def __str__(self):
        return f"{self.name} - ${self.price}, Stock: {self.stock}"

class User:
    def __init__(self, username):
        self.username = username
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"User: {self.username}, Orders: {len(self.orders)}"

class Order:
    def __init__(self, user, product, quantity):
        if quantity > product.stock:
            raise ValueError("Not enough stock to fulfill order")
        self.user = user
        self.product = product
        self.quantity = quantity
        self.total_price = self.product.price * self.quantity
        self.status = "Pending"

        # Update stock in product
        product.update_stock(-quantity)

    def complete_order(self):
        if self.status == "Completed":
            raise ValueError("Order is already completed")
        self.status = "Completed"

    def __str__(self):
        return f"Order by {self.user.username} for {self.quantity} x {self.product.name} - Status: {self.status}"

class Store:
    def __init__(self):
        self.products = []
        self.users = []
        self.orders = []

    def add_product(self, product):
        self.products.append(product)

    def add_user(self, user):
        self.users.append(user)

    def find_product(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None

    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def create_order(self, username, product_name, quantity):
        user = self.find_user(username)
        if not user:
            raise ValueError("User not found")
        product = self.find_product(product_name)
        if not product:
            raise ValueError("Product not found")

        order = Order(user, product, quantity)
        user.add_order(order)
        self.orders.append(order)
        return order

    def complete_order(self, order_id):
        if order_id >= len(self.orders):
            raise ValueError("Order not found")
        order = self.orders[order_id]
        order.complete_order()

class ReportGenerator:
    @staticmethod
    def generate_sales_report(store):
        report = "Sales Report\n"
        report += "=" * 20 + "\n"
        for product in store.products:
            sold_quantity = sum(
                order.quantity for order in store.orders if order.product == product
            )
            report += f"{product.name} - Sold: {sold_quantity}, Remaining Stock: {product.stock}\n"
        return report

    @staticmethod
    def generate_user_report(user):
        report = f"User Report for {user.username}\n"
        report += "=" * 20 + "\n"
        for order in user.orders:
            report += f"{order}\n"
        return report

# example_usage.py

from store_management import Store, Product, User, ReportGenerator

# Инициализация магазина
store = Store()

# Добавление товаров
product1 = Product("Laptop", 1000, 10)
product2 = Product("Phone", 500, 20)
store.add_product(product1)
store.add_product(product2)

# Добавление пользователей
user1 = User("Alice")
user2 = User("Bob")
store.add_user(user1)
store.add_user(user2)

# Создание заказов
order1 = store.create_order("Alice", "Laptop", 2)
order2 = store.create_order("Bob", "Phone", 1)

# Завершение заказов
store.complete_order(0)

# Генерация отчетов
print(ReportGenerator.generate_sales_report(store))
print(ReportGenerator.generate_user_report(user1))
print(ReportGenerator.generate_user_report(user2))

# test_store_management.py

import unittest
from store_management import Store, Product, User, Order

class TestStoreManagement(unittest.TestCase):

    def setUp(self):
        # Arrange: Создаем магазин, добавляем товары и пользователей
        self.store = Store()
        self.product1 = Product("Laptop", 1000, 10)
        self.product2 = Product("Phone", 500, 20)
        self.user = User("Alice")
        self.user2 = User("Bob")

        # Добавляем товары и пользователей в магазин
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)
        self.store.add_user(self.user)
        self.store.add_user(self.user2)

    def test_add_product(self):
        # Arrange - Подготовлено в setUp

        # Act: Прямое действие не требуется, так как проверяем состояние магазина после добавления товаров

        # Assert: Проверка, что товары были добавлены в магазин
        self.assertIn(self.product1, self.store.products)
        self.assertIn(self.product2, self.store.products)

    def test_create_order(self):
        # Arrange: Находим пользователя и товар
        username = "Alice"
        product_name = "Laptop"
        quantity = 2

        # Act: Создаем заказ
        order = self.store.create_order(username, product_name, quantity)

        # Assert: Проверка корректности заказа и обновления состояния
        self.assertEqual(order.quantity, quantity)               # Количество товара в заказе
        self.assertEqual(order.total_price, 2000)                # Общая стоимость заказа
        self.assertEqual(self.product1.stock, 8)                # Уменьшение запаса товара на складе

    def test_complete_order(self):
        # Arrange: Создаем заказ, который можно завершить
        order = self.store.create_order("Alice", "Phone", 1)

        # Act: Завершаем заказ
        self.store.complete_order(0)

        # Assert: Проверка, что статус заказа изменился на "Completed"
        self.assertEqual(order.status, "Completed")

    def test_insufficient_stock(self):
        # Arrange: Пытаемся заказать больше, чем имеется на складе
        username = "Alice"
        product_name = "Laptop"
        excessive_quantity = 11

        # Act & Assert: Проверка, что при недостаточном количестве товара возникает ошибка
        with self.assertRaises(ValueError):
            self.store.create_order(username, product_name, excessive_quantity)

    def test_update_stock_after_multiple_orders(self):
        # Arrange: Заказы от двух пользователей на один и тот же товар
        initial_stock = self.product1.stock
        order1_quantity = 3
        order2_quantity = 4

        # Act: Создаем два заказа на один товар
        self.store.create_order("Alice", "Laptop", order1_quantity)
        self.store.create_order("Bob", "Laptop", order2_quantity)

        # Assert: Проверка, что запас уменьшился на общую сумму заказов
        expected_stock = initial_stock - (order1_quantity + order2_quantity)
        self.assertEqual(self.product1.stock, expected_stock)

if __name__ == "__main__":
    unittest.main()

import unittest
from store_management import Store, Product, User, Order,ReportGenerator

class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Создаем магазин и начальные данные
        self.store = Store()
        self.product1 = Product("Laptop", 1000, 10)
        self.product2 = Product("Mouse", 50, 50)
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)

        self.user1 = User("user123")
        self.store.add_user(self.user1)

    # 1. Тест создания заказа и обновления остатка
    def test_create_order_and_update_stock(self):
        order = self.store.create_order("user123", "Laptop", 2)
        self.assertEqual(order.product.stock, 8)  # Было 10, вычли 2
        self.assertEqual(len(self.user1.orders), 1)
        self.assertEqual(order.status, "Pending")

    # 2. Тест создания заказа с недостаточным количеством товара
    def test_create_order_insufficient_stock(self):
        with self.assertRaises(ValueError):
            self.store.create_order("user123", "Laptop", 20)  # Не хватает товара

    # 3. Тест завершения заказа
    def test_complete_order(self):
        order = self.store.create_order("user123", "Mouse", 5)
        self.store.complete_order(0)  # Завершаем первый заказ
        self.assertEqual(order.status, "Completed")

    # 4. Тест отчетов о продажах
    def test_generate_sales_report(self):
        self.store.create_order("user123", "Laptop", 2)
        report = ReportGenerator.generate_sales_report(self.store)
        expected_report = (
            "Sales Report\n"
            "====================\n"
            "Laptop - Sold: 2, Remaining Stock: 8\n"
            "Mouse - Sold: 0, Remaining Stock: 50\n"
        )
        self.assertEqual(report.strip(), expected_report.strip())

    # 5. Тест отчетов пользователя
    def test_generate_user_report(self):
        self.store.create_order("user123", "Mouse", 3)
        report = ReportGenerator.generate_user_report(self.user1)
        self.assertIn("Order by user123 for 3 x Mouse", report)

if __name__ == "__main__":
    unittest.main()

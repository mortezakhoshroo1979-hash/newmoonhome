from decimal import Decimal
from django.test import TestCase
from products.models import Category, Product


class ProductModelTest(TestCase):
    def test_calculate_price(self):
        category = Category.objects.create(name='مبلمان')
        product = Product.objects.create(
            category=category,
            name='محصول تست',
            description='توضیحات',
            base_price=Decimal('1000000'),
            sku='TEST-001',
            customization_fields={
                'options': [
                    {
                        'group': 'size',
                        'items': [
                            {'value': 'large', 'price_adjustment': 200000}
                        ]
                    }
                ]
            }
        )
        self.assertEqual(product.calculate_price({'size': 'large'}), Decimal('1200000'))

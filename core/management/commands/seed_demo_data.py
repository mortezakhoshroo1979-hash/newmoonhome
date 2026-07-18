import io
import os
import urllib.request
from decimal import Decimal
from django.core.files import File
from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product, ProductImage


class Command(BaseCommand):
    help = 'ایجاد داده‌های نمونه (۳ دسته‌بندی، ۱ برند، ۸ محصول با تصاویر اختصاصی لوکس)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('در حال ایجاد دسته‌بندی‌ها...'))
        cat1, _ = Category.objects.get_or_create(
            slug='furniture',
            defaults={'name': 'مبلمان', 'description': 'انواع مبلمان لوکس راحتی، کلاسیک و ال', 'is_active': True}
        )
        cat2, _ = Category.objects.get_or_create(
            slug='bedrooms',
            defaults={'name': 'سرویس خواب', 'description': 'سرویس خواب، تخت، پاتختی و دراور چوبی', 'is_active': True}
        )
        cat3, _ = Category.objects.get_or_create(
            slug='tables-consoles',
            defaults={'name': 'میز و کنسول', 'description': 'میز ناهارخوری، جلو مبلی و کنسول‌های مدرن', 'is_active': True}
        )
        categories = [cat1, cat2, cat3]
        self.stdout.write(self.style.SUCCESS(f'۳ دسته‌بندی ایجاد/بررسی شد: {[c.name for c in categories]}'))

        self.stdout.write(self.style.NOTICE('در حال ایجاد برند...'))
        logo_path = '/home/user/static/assets/logo.png'
        if not os.path.exists(logo_path):
            logo_path = '/home/user/forest_hero_insert.png'

        brand, brand_created = Brand.objects.get_or_create(
            slug='newmoon',
            defaults={
                'name': 'NEWMOON',
                'description': 'برند انحصاری طراحی و تولید محصولات چوبی لوکس NEWMOON HOME',
                'website': 'https://newmoonhome.ir',
                'is_active': True,
            }
        )
        if brand_created and os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                brand.logo.save('newmoon_brand.png', File(f), save=True)
        self.stdout.write(self.style.SUCCESS(f'برند ایجاد/بررسی شد: {brand.name}'))

        demo_products = [
            {
                'name': 'مبل راحتی چستر نیومون',
                'slug': 'chester-sofa-newmoon',
                'sku': 'NMH-PROD-101',
                'category': cat1,
                'base_price': Decimal('45000000'),
                'special_price': Decimal('42000000'),
                'stock': 5,
                'is_featured': True,
                'description': 'مبل راحتی سه‌نفره چستر با روکش مخمل درجه یک و پایه‌های چوب راش طبیعی.'
            },
            {
                'name': 'مبل ال و ماژولار آتریا',
                'slug': 'atria-modular-sofa',
                'sku': 'NMH-PROD-102',
                'category': cat1,
                'base_price': Decimal('68000000'),
                'special_price': None,
                'stock': 3,
                'is_featured': True,
                'description': 'طراحی ماژولار انعطاف‌پذیر مناسب برای سالن‌های پذیرایی مدرن و بزرگ.'
            },
            {
                'name': 'تخت خواب دو نفره کینگ چوبی',
                'slug': 'wooden-king-bed',
                'sku': 'NMH-PROD-103',
                'category': cat2,
                'base_price': Decimal('38000000'),
                'special_price': Decimal('35000000'),
                'stock': 8,
                'is_featured': True,
                'description': 'تخت خواب دونفره سایز کینگ ساخته شده از چوب طبیعی گردو با اتصالات کام و زبانه.'
            },
            {
                'name': 'میز ناهارخوری ۶ نفره مون',
                'slug': 'moon-dining-table',
                'sku': 'NMH-PROD-104',
                'category': cat3,
                'base_price': Decimal('34000000'),
                'special_price': None,
                'stock': 4,
                'is_featured': False,
                'description': 'میز ناهارخوری مستطیلی با سطح چوب یکپارچه و مقاومت بالا در برابر رطوبت و حرارت.'
            },
            {
                'name': 'میز جلو مبلی چوب گردو',
                'slug': 'walnut-coffee-table',
                'sku': 'NMH-PROD-105',
                'category': cat3,
                'base_price': Decimal('12500000'),
                'special_price': Decimal('11000000'),
                'stock': 10,
                'is_featured': False,
                'description': 'میز جلو مبلی با طراحی ارگانیک و پرداخت روغنی طبیعی برای حفظ بافت چوب.'
            },
            {
                'name': 'میز کنسول چوبی مدل آرتین',
                'slug': 'artin-wooden-console',
                'sku': 'NMH-PROD-106',
                'category': cat3,
                'base_price': Decimal('31500000'),
                'special_price': None,
                'stock': 6,
                'is_featured': True,
                'description': 'کنسول لوکس ۴ درب با فضای ذخیره‌سازی جادار و دستگیره‌های برنجی سفارشی.'
            },
            {
                'name': 'پاتختی چوبی مینیمال',
                'slug': 'minimal-nightstand',
                'sku': 'NMH-PROD-107',
                'category': cat2,
                'base_price': Decimal('8500000'),
                'special_price': None,
                'stock': 15,
                'is_featured': False,
                'description': 'پاتختی دو کشو با ریل‌های آرام‌بند مخفی و طراحی مینیمال اسکاندیناوی.'
            },
            {
                'name': 'صندلی تک‌نفره لانج لوکس',
                'slug': 'luxury-lounge-chair',
                'sku': 'NMH-PROD-108',
                'category': cat1,
                'base_price': Decimal('18000000'),
                'special_price': Decimal('16500000'),
                'stock': 7,
                'is_featured': False,
                'description': 'صندلی ارگونومیک تک‌نفره با پشتی بلند و نشیمن فوم سرد با دانسیته بالا.'
            },
        ]

        self.stdout.write(self.style.NOTICE('در حال ایجاد ۸ محصول نمونه...'))
        created_count = 0
        for item in demo_products:
            prod, created = Product.objects.get_or_create(
                sku=item['sku'],
                defaults={
                    'name': item['name'],
                    'slug': item['slug'],
                    'category': item['category'],
                    'brand': brand,
                    'base_price': item['base_price'],
                    'special_price': item['special_price'],
                    'stock': item['stock'],
                    'is_featured': item['is_featured'],
                    'is_active': True,
                    'description': item['description'],
                }
            )
            prod.name = item['name']
            prod.slug = item['slug']
            prod.is_active = True
            prod.is_featured = item['is_featured']
            prod.base_price = item['base_price']
            prod.special_price = item['special_price']
            prod.save()

            if created:
                created_count += 1

            img_obj = prod.images.filter(is_feature=True).first() or prod.images.first()
            if not img_obj or 'NMH-PROD' not in str(img_obj.image.name) or not os.path.exists(img_obj.image.path):
                try:
                    from PIL import Image, ImageDraw
                    colors = [
                        (26, 60, 42),   # Forest Green
                        (44, 30, 20),   # Walnut Brown
                        (20, 32, 48),   # Midnight Blue
                        (50, 42, 34),   # Charcoal Oak
                        (38, 54, 40),   # Emerald Wood
                        (56, 40, 28),   # Mahogany
                        (28, 44, 48),   # Sage
                        (48, 36, 30),   # Teak
                    ]
                    idx = int(prod.sku.split('-')[-1]) % len(colors)
                    bg_color = colors[idx]
                    img_pil = Image.new('RGB', (800, 600), color=bg_color)
                    draw = ImageDraw.Draw(img_pil)
                    
                    # Gold border frame
                    draw.rectangle([20, 20, 780, 580], outline=(201, 168, 76), width=4)
                    draw.rectangle([32, 32, 768, 568], outline=(201, 168, 76), width=1)
                    
                    # Luxury Gold Accent Banner in center
                    draw.rectangle([150, 240, 650, 360], fill=(201, 168, 76))
                    
                    buf = io.BytesIO()
                    img_pil.save(buf, format='JPEG', quality=92)
                    buf.seek(0)
                    
                    if not img_obj:
                        img_obj = ProductImage(product=prod, alt_text=prod.name, is_feature=True, sort_order=1)
                    img_obj.image.save(f'{prod.sku}_luxury.jpg', File(buf), save=True)
                except Exception as e:
                    if os.path.exists(logo_path) and not img_obj:
                        with open(logo_path, 'rb') as f:
                            img = ProductImage(product=prod, alt_text=prod.name, is_feature=True, sort_order=1)
                            img.image.save(f'{prod.sku}.png', File(f), save=True)

        self.stdout.write(self.style.SUCCESS(f'تعداد محصولات جدید ایجاد شده: {created_count} | مجموع محصولات اکنون: {Product.objects.count()}'))

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='کد')),
                ('discount_type', models.CharField(choices=[('percent', 'درصدی'), ('fixed', 'ثابت')], max_length=20, verbose_name='نوع تخفیف')),
                ('value', models.DecimalField(decimal_places=0, max_digits=12, verbose_name='مقدار تخفیف')),
                ('min_order_amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='حداقل مبلغ سفارش')),
                ('max_discount_amount', models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True, verbose_name='حداکثر مبلغ تخفیف')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضا')),
                ('max_uses', models.PositiveIntegerField(default=1, verbose_name='حداکثر استفاده')),
                ('used_count', models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryDiscount',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='عنوان')),
                ('percent', models.PositiveSmallIntegerField(verbose_name='درصد تخفیف')),
                ('start_date', models.DateTimeField(verbose_name='تاریخ شروع')),
                ('end_date', models.DateTimeField(verbose_name='تاریخ پایان')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='products.category', verbose_name='دستهبندی')),
            ],
        ),
        migrations.CreateModel(
            name='BulkPriceUpdate',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('update_type', models.CharField(choices=[('percent', 'درصدی'), ('fixed', 'مبلغ ثابت')], max_length=20, verbose_name='نوع تغییر')),
                ('value', models.DecimalField(decimal_places=0, max_digits=12, verbose_name='مقدار')),
                ('status', models.CharField(choices=[('draft', 'پیشنویس'), ('scheduled', 'زمانبندیشده'), ('applied', 'اعمالشده'), ('canceled', 'لغوشده')], default='draft', max_length=20, verbose_name='وضعیت')),
                ('scheduled_at', models.DateTimeField(blank=True, null=True, verbose_name='زمان اجرا')),
                ('note', models.TextField(blank=True, verbose_name='توضیحات')),
                ('brands', models.ManyToManyField(blank=True, related_name='bulk_price_updates', to='products.brand', verbose_name='برندها')),
                ('categories', models.ManyToManyField(blank=True, related_name='bulk_price_updates', to='products.category', verbose_name='دستهبندیها')),
                ('products', models.ManyToManyField(blank=True, related_name='bulk_price_updates', to='products.product', verbose_name='محصولات')),
            ],
        ),
    ]

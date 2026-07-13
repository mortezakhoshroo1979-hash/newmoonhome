from django.db import migrations, models
import django.db.models.deletion
import uuid
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('discounts', '0001_initial'),
        ('products', '0001_initial'),
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_number', models.CharField(blank=True, max_length=50, unique=True, verbose_name='شماره سفارش')),
                ('status', models.CharField(choices=[('registered', 'ثبت'), ('confirmed', 'تایید'), ('preparing', 'آمادهسازی'), ('shipped', 'ارسال'), ('delivered', 'تحویل'), ('canceled', 'لغو'), ('returned', 'مرجوعی')], default='registered', max_length=20, verbose_name='وضعیت')),
                ('subtotal_amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='جمع جزء')),
                ('discount_amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='مبلغ تخفیف')),
                ('shipping_amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='هزینه ارسال')),
                ('total_amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='مبلغ نهایی')),
                ('receiver_name', models.CharField(max_length=255, verbose_name='نام گیرنده')),
                ('receiver_phone', models.CharField(max_length=20, verbose_name='شماره گیرنده')),
                ('province', models.CharField(max_length=100, verbose_name='استان')),
                ('city', models.CharField(max_length=100, verbose_name='شهر')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('postal_code', models.CharField(blank=True, max_length=20, verbose_name='کد پستی')),
                ('customer_note', models.TextField(blank=True, verbose_name='یادداشت مشتری')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='زمان پرداخت')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='discounts.coupon', verbose_name='کوپن')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shipping.shippingmethod', verbose_name='روش ارسال')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='accounts.user', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255, verbose_name='نام محصول')),
                ('sku', models.CharField(blank=True, max_length=100, verbose_name='SKU')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='تعداد')),
                ('selected_options', models.JSONField(blank=True, default=dict, verbose_name='گزینههای انتخابی')),
                ('unit_price_snapshot', models.DecimalField(decimal_places=0, max_digits=12, verbose_name='قیمت واحد در لحظه ثبت')),
                ('total_price_snapshot', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='قیمت کل در لحظه ثبت')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='سفارش')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='products.product', verbose_name='محصول')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatusHistory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('from_status', models.CharField(choices=[('registered', 'ثبت'), ('confirmed', 'تایید'), ('preparing', 'آمادهسازی'), ('shipped', 'ارسال'), ('delivered', 'تحویل'), ('canceled', 'لغو'), ('returned', 'مرجوعی')], max_length=20, verbose_name='از وضعیت')),
                ('to_status', models.CharField(choices=[('registered', 'ثبت'), ('confirmed', 'تایید'), ('preparing', 'آمادهسازی'), ('shipped', 'ارسال'), ('delivered', 'تحویل'), ('canceled', 'لغو'), ('returned', 'مرجوعی')], max_length=20, verbose_name='به وضعیت')),
                ('note', models.TextField(blank=True, verbose_name='توضیحات')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='changed_order_statuses', to='accounts.user', verbose_name='تغییردهنده')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='orders.order', verbose_name='سفارش')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(blank=True, max_length=50, unique=True, verbose_name='شماره فاکتور')),
                ('issue_date', models.DateField(default=django.utils.timezone.localdate, verbose_name='تاریخ صدور')),
                ('legal_name', models.CharField(blank=True, max_length=255, verbose_name='نام حقوقی/حقیقی')),
                ('economic_code', models.CharField(blank=True, max_length=50, verbose_name='کد اقتصادی')),
                ('national_id', models.CharField(blank=True, max_length=50, verbose_name='شناسه/کد ملی')),
                ('amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='مبلغ')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='orders.order', verbose_name='سفارش')),
            ],
        ),
    ]

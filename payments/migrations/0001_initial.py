from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام درگاه')),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True, verbose_name='اسلاگ')),
                ('provider', models.CharField(max_length=100, verbose_name='ارائهدهنده')),
                ('settings_json', models.JSONField(blank=True, default=dict, verbose_name='تنظیمات JSON')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('priority', models.PositiveIntegerField(default=0, verbose_name='اولویت')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=12, verbose_name='مبلغ')),
                ('status', models.CharField(choices=[('pending', 'در انتظار'), ('success', 'موفق'), ('failed', 'ناموفق'), ('canceled', 'لغو شده'), ('refunded', 'بازپرداخت شده')], default='pending', max_length=20, verbose_name='وضعیت')),
                ('authority', models.CharField(blank=True, max_length=255, verbose_name='Authority')),
                ('reference_id', models.CharField(blank=True, max_length=255, verbose_name='Reference ID')),
                ('tracking_code', models.CharField(blank=True, max_length=255, verbose_name='کد پیگیری')),
                ('card_pan', models.CharField(blank=True, max_length=30, verbose_name='شماره کارت ماسکشده')),
                ('raw_response', models.JSONField(blank=True, default=dict, verbose_name='پاسخ خام درگاه')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='زمان پرداخت')),
                ('gateway', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='payments.paymentgateway', verbose_name='درگاه')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='orders.order', verbose_name='سفارش')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='accounts.user', verbose_name='کاربر')),
            ],
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='نام')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('base_cost', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='هزینه پایه')),
                ('cost_per_kg', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='هزینه هر کیلوگرم')),
                ('min_weight', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='حداقل وزن')),
                ('max_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='حداکثر وزن')),
                ('covered_cities', models.JSONField(blank=True, default=list, verbose_name='شهرهای تحت پوشش')),
                ('delivery_time', models.CharField(max_length=150, verbose_name='زمان تحویل')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingRate',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('province', models.CharField(max_length=100, verbose_name='استان')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='شهر')),
                ('extra_cost', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='هزینه اضافی')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('shipping_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_rates', to='shipping.shippingmethod', verbose_name='روش ارسال')),
            ],
        ),
    ]

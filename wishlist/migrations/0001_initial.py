from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('products', models.ManyToManyField(blank=True, related_name='wishlists', to='products.product', verbose_name='محصولات')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='accounts.user', verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('products', models.ManyToManyField(blank=True, related_name='compare_lists', to='products.product', verbose_name='محصولات')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='compare_list', to='accounts.user', verbose_name='کاربر')),
            ],
        ),
    ]

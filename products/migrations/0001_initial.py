from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='نام برند')),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True, verbose_name='اسلاگ')),
                ('logo', models.ImageField(upload_to='products/brands/', verbose_name='لوگو')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('website', models.URLField(blank=True, verbose_name='وبسایت')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={'verbose_name': 'برند', 'verbose_name_plural': 'برندها', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, verbose_name='نام دسته')),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True, verbose_name='اسلاگ')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/categories/', verbose_name='تصویر')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category', verbose_name='دسته والد')),
            ],
            options={'verbose_name': 'دستهبندی', 'verbose_name_plural': 'دستهبندیها', 'ordering': ['name'], 'unique_together': {('parent', 'name')}},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='نام محصول')),
                ('slug', models.SlugField(blank=True, max_length=280, unique=True, verbose_name='اسلاگ')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('base_price', models.DecimalField(decimal_places=0, max_digits=12, verbose_name='قیمت پایه')),
                ('special_price', models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True, verbose_name='قیمت ویژه')),
                ('sku', models.CharField(max_length=100, unique=True, verbose_name='SKU')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='وزن (کیلوگرم)')),
                ('dimensions', models.CharField(blank=True, max_length=255, verbose_name='ابعاد')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='موجودی پایه')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_featured', models.BooleanField(default=False, verbose_name='ویژه')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')),
                ('sales_count', models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')),
                ('customization_fields', models.JSONField(blank=True, default=dict, verbose_name='فیلدهای شخصیسازی')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.brand', verbose_name='برند')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category', verbose_name='دستهبندی')),
            ],
            options={'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='products/images/', verbose_name='تصویر')),
                ('alt_text', models.CharField(blank=True, max_length=255, verbose_name='متن جایگزین')),
                ('is_feature', models.BooleanField(default=False, verbose_name='تصویر شاخص')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='محصول')),
            ],
            options={'verbose_name': 'تصویر محصول', 'verbose_name_plural': 'تصاویر محصولات', 'ordering': ['sort_order', 'created_at']},
        ),
        migrations.CreateModel(
            name='ProductThreeD',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='عنوان')),
                ('file', models.FileField(upload_to='products/3d/', verbose_name='فایل سهبعدی')),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to='products/3d/previews/', verbose_name='تصویر پیشنمایش')),
                ('file_format', models.CharField(blank=True, max_length=50, verbose_name='فرمت فایل')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='three_d_files', to='products.product', verbose_name='محصول')),
            ],
            options={'verbose_name': 'فایل سهبعدی محصول', 'verbose_name_plural': 'فایلهای سهبعدی محصولات', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='عنوان')),
                ('video', models.FileField(upload_to='products/videos/', verbose_name='فایل ویدیو')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='products/videos/thumbnails/', verbose_name='تصویر بندانگشتی')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='products.product', verbose_name='محصول')),
            ],
            options={'verbose_name': 'ویدیوی محصول', 'verbose_name_plural': 'ویدیوهای محصولات', 'ordering': ['sort_order', 'created_at']},
        ),
        migrations.AddIndex(model_name='product', index=models.Index(fields=['slug'], name='products_pr_slug_6f31be_idx')),
        migrations.AddIndex(model_name='product', index=models.Index(fields=['sku'], name='products_pr_sku_904f20_idx')),
        migrations.AddIndex(model_name='product', index=models.Index(fields=['is_active', 'is_featured'], name='products_pr_is_acti_f4a354_idx')),
    ]

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='نام')),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True, verbose_name='اسلاگ')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام')),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True, verbose_name='اسلاگ')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('slug', models.SlugField(blank=True, max_length=280, unique=True, verbose_name='اسلاگ')),
                ('excerpt', models.TextField(blank=True, verbose_name='خلاصه')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='blog/posts/', verbose_name='تصویر شاخص')),
                ('seo_title', models.CharField(blank=True, max_length=255, verbose_name='عنوان سئو')),
                ('seo_description', models.TextField(blank=True, verbose_name='توضیحات سئو')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')),
                ('status', models.CharField(choices=[('draft', 'پیشنویس'), ('published', 'منتشر شده')], default='draft', max_length=20, verbose_name='وضعیت')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='زمان انتشار')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='accounts.user', verbose_name='نویسنده')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.postcategory', verbose_name='دستهبندی')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='blog.tag', verbose_name='تگها')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='نام')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='ایمیل')),
                ('body', models.TextField(verbose_name='متن نظر')),
                ('is_approved', models.BooleanField(default=False, verbose_name='تایید شده')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment', verbose_name='والد')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='پست')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_comments', to='accounts.user', verbose_name='کاربر')),
            ],
        ),
    ]

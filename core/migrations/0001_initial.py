from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('site_name', models.CharField(default='NEW MOON HOME', max_length=255, verbose_name='عنوان سایت')),
                ('site_description', models.TextField(blank=True, verbose_name='توضیحات سایت')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='core/settings/', verbose_name='لوگو')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='core/settings/', verbose_name='فاوآیکون')),
                ('primary_color', models.CharField(default='#1a3c2a', max_length=7, verbose_name='رنگ اصلی')),
                ('secondary_color', models.CharField(default='#c9a84c', max_length=7, verbose_name='رنگ ثانویه')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='تلفن تماس')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='ایمیل تماس')),
                ('address', models.TextField(blank=True, verbose_name='آدرس')),
                ('social_links', models.JSONField(blank=True, default=dict, verbose_name='شبکههای اجتماعی')),
                ('seo_meta', models.JSONField(blank=True, default=dict, verbose_name='تنظیمات سئو')),
            ],
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralTransaction',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reward_amount', models.DecimalField(decimal_places=0, default=0, max_digits=12, verbose_name='مبلغ پاداش')),
                ('note', models.TextField(blank=True, verbose_name='توضیحات')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referral_transactions', to='orders.order', verbose_name='سفارش')),
                ('referral_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.referralcode', verbose_name='کد معرف')),
                ('referred_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals_received', to='accounts.user', verbose_name='کاربر معرفیشده')),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals_made', to='accounts.user', verbose_name='معرف')),
            ],
        ),
    ]

import random

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile, ReferralCode, User


@receiver(post_save, sender=User)
def create_profile_and_referral(sender, instance, created, **kwargs):
    """پس از ایجاد کاربر، پروفایل و کد معرف ساخته می‌شود."""
    if created:
        Profile.objects.get_or_create(user=instance)
        if not hasattr(instance, 'referral_code'):
            code = f'NMH-{random.randint(100000, 999999)}'
            ReferralCode.objects.get_or_create(user=instance, defaults={'code': code})

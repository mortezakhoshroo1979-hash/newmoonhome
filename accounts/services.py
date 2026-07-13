from django.db import transaction

from accounts.models import CustomerRank, ReferralCode, ReferralTransaction


class LoyaltyService:
    """سرویس مربوط به امتیاز و ارتقای سطح مشتری."""

    @staticmethod
    @transaction.atomic
    def assign_points_for_order(order):
        if not order.user or order.status != 'delivered':
            return 0
        profile = getattr(order.user, 'profile', None)
        if not profile:
            return 0

        points = int(order.total_amount // 1000000)
        profile.score += points
        profile.rank = CustomerRank.objects.filter(
            minimum_score__lte=profile.score,
            is_active=True,
        ).order_by('-minimum_score').first()
        profile.save(update_fields=['score', 'rank', 'updated_at'])
        return points


class ReferralService:
    """سرویس سیستم کد معرف."""

    @staticmethod
    @transaction.atomic
    def apply_referral_after_first_order(order, referral_code_value=None):
        if not order.user or not referral_code_value:
            return None
        referral_code = ReferralCode.objects.filter(code=referral_code_value, is_active=True).select_related('user').first()
        if not referral_code or referral_code.user_id == order.user_id:
            return None

        exists = ReferralTransaction.objects.filter(referred_user=order.user).exists()
        if exists:
            return None

        reward_amount = 500000
        referral_code.usage_count += 1
        referral_code.total_reward_amount += reward_amount
        referral_code.save(update_fields=['usage_count', 'total_reward_amount', 'updated_at'])

        return ReferralTransaction.objects.create(
            referral_code=referral_code,
            referrer=referral_code.user,
            referred_user=order.user,
            order=order,
            reward_amount=reward_amount,
            note='ثبت خودکار پس از اولین خرید موفق',
        )

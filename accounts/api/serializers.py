from rest_framework import serializers
from accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    rank = serializers.CharField(source='profile.rank.name', read_only=True)
    score = serializers.IntegerField(source='profile.score', read_only=True)
    referral_code = serializers.CharField(source='referral_code.code', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_verified', 'rank', 'score', 'referral_code']

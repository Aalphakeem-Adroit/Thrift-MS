from rest_framework import serializers
from .models import ThriftGroup, Membership, Contribution, Payout

class ThriftGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThriftGroup
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = '__all__'

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = '__all__'
from app.core.models.customer.entity import MRewardsTransaction, MCreditBalance
from rest_framework import serializers


class RewardPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = MRewardsTransaction
        fields = ("transaction_id", "customer", "amount",
                  "amount_used", "comment", "code", "created_at", "updated_at")


class McreditBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MCreditBalance
        fields = ("balance_id", "customer", "amount",
                  "is_subscribed", "created_at", "updated_at")

from app.core.models.customer.entity import MRewardsTransaction
from rest_framework import serializers

class RewardPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MRewardsTransaction
        fields = ("transaction_id", "customer","amount", "amount_used", "comment", "code", "created_at", "updated_at")
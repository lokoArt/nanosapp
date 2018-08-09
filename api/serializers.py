from rest_framework import serializers

from api.models import AdSet


class AdSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSet
        fields = ('id',
                  'name',
                  'goal',
                  'total_budget',
                  'status',
                  'platforms')

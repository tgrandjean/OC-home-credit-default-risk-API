from rest_framework import serializers
from api.models import Application


class PredictionSerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    amt = serializers.FloatField()
    amt_annuity = serializers.FloatField()


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""

    class Meta:
        model = Application
        fields = '__all__'

from rest_framework import serializers
from api.models import Application


class PredictionSerializer(serializers.Serializer):
    sk_id_curr = serializers.IntegerField(help_text='ID of the application')
    amt_credit = serializers.FloatField(help_text='Credit amount')
    amt_annuity = serializers.FloatField(help_text='Annuity amount')


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""

    class Meta:
        model = Application
        fields = '__all__'

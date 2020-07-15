from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    amt = serializers.FloatField()
    amt_annuity = serializers.FloatField()

import pickle
import os
import pandas as pd

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.serializers import PredictionSerializer

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
# Create your views here.

class Predict(APIView):
    """Endpoint for prediction.

    receive data from POST and return refund probability.
    """
    serializer_class = PredictionSerializer

    def post(self, request):
        with open(os.path.join(settings.BASE_DIR, 'models', 'model.pickle'), 'rb') as f:
            m = pickle.load(f)
        data = PredictionSerializer(data=request.data)
        data.is_valid()
        sk_id_curr = data.data['app_id']
        amt = data.data['amt']
        amt_annuity = data.data['amt_annuity']
        data = pd.read_csv(os.path.join(settings.BASE_DIR, 'models', 'test.csv'))
        data.set_index('SK_ID_CURR', inplace=True)
        res = {"score": (1 - m.predict(data.loc[sk_id_curr])[0]) * 100}
        return Response(res)


class Application(APIView):
    """Endpoint for application.

    return data relative to an application.
    """
    def get(self, request, pk):
        app_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'models', 'test.csv'))
        app_data.set_index('SK_ID_CURR', inplace=True)
        return Response(app_data.loc[pk].to_dict())

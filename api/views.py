import pickle
import os
import numpy as np
import pandas as pd

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.serializers import PredictionSerializer, ApplicationSerializer
from api.models import Application


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your views here.

def infer(data):
    print('Make inference')
    data = pd.DataFrame(data).T
    with open(os.path.join(settings.BASE_DIR, 'models', 'model_V0.pickle'),
              'rb') as f:
          model = pickle.load(f)
    with open(os.path.join(settings.BASE_DIR, 'models',
                           'preprocessing_pipeline.pickle'), 'rb') as f:
          preprocessing_pipeline = pickle.load(f)
    data = preprocessing_pipeline.transform(data)
    prob = model.predict_proba(data)
    return prob[:, 1][0]


class Predict(APIView):
    """Endpoint for prediction.

    receive data from POST and return refund probability.
    """
    serializer_class = PredictionSerializer

    def post(self, request):
        data = PredictionSerializer(data=request.data)
        data.is_valid()
        sk_id_curr = data.data['app_id']
        amt = data.data['amt']
        amt_annuity = data.data['amt_annuity']
        data = pd.read_csv(os.path.join(settings.BASE_DIR,
                           'models', 'features_final.csv'))
        data.set_index('SK_ID_CURR', inplace=True)
        data.drop(columns='TARGET', inplace=True)
        input_data = data.loc[sk_id_curr].copy()
        input_data['AMT_CREDIT'] = amt
        input_data['AMT_ANNUITY'] = amt_annuity
        prob = infer(input_data)
        res = {"refund probability": (1 - prob) * 100}
        return Response(res)


class ApplicationViewSet(viewsets.ModelViewSet):
    """End point for application management."""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

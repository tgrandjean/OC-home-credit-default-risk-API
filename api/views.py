import pickle
import os
import numpy as np
import pandas as pd

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
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
    data = pd.DataFrame(data).T
    with open(os.path.join(settings.BASE_DIR, 'models', 'model_v0.pickle'),
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
        sk_id_curr = data.data['sk_id_curr']
        amt = data.data['amt_credit']
        amt_annuity = data.data['amt_annuity']
        app = get_object_or_404(Application, pk=sk_id_curr)
        data = pd.DataFrame.from_records([model_to_dict(app)])
        data.columns = [x.upper() for x in data.columns]
        cols = []
        for col in data.columns:
            if col.endswith('_ACTIVE'):
                col = col.replace('_ACTIVE_ACTIVE', '_ACTIVE_Active')
            elif col.endswith('_CLOSED'):
                col = col.replace('_CLOSED', '_Closed')
            cols.append(col)
        data.columns = cols
        data.set_index('SK_ID_CURR', inplace=True)
        data['AMT_CREDIT'] = amt
        data['AMT_ANNUITY'] = amt_annuity
        prob = infer(data.T)
        res = dict()
        res['input data'] = data
        res['Model response'] = (1 - prob) * 100
        return Response(res)


class ApplicationViewSet(viewsets.ModelViewSet):
    """End point for application management."""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

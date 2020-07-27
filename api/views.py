import pickle
import os
from random import randint
import numpy as np
import pandas as pd

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import shap

from api.serializers import PredictionSerializer, ApplicationSerializer
from api.models import Application
from api.filters import ApplicationFilter

ORDERED_COLS = ['DAYS_BIRTH',
                'OCCUPATION_TYPE',
                'AMT_INCOME_TOTAL',
                'AMT_CREDIT',
                'NAME_CONTRACT_TYPE',
                'AMT_ANNUITY',
                'EXT_SOURCE_1',
                'EXT_SOURCE_2',
                'EXT_SOURCE_3',
                'CREDIT_ACTIVE_Active',
                'CREDIT_ACTIVE_Closed',
                'REPORTED_DPD',
                'BAD_PAYMENT_HC',
                'ACTIVE_CRED_HC',
                'TOTAL_PREV_HC']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def infer(data, transform_only=False):
    data = pd.DataFrame(data)
    with open(os.path.join(settings.BASE_DIR, 'models', 'model_v0.pickle'),
              'rb') as f:
          model = pickle.load(f)
    with open(os.path.join(settings.BASE_DIR, 'models',
                           'preprocessing_pipeline.pickle'), 'rb') as f:
          preprocessing_pipeline = pickle.load(f)
    data = preprocessing_pipeline.transform(data)
    if transform_only:
        return data, preprocessing_pipeline, model
    else:
        prob = model.predict_proba(data)
        return prob[:, 1][0]


def capitalize_column_names(dataframe):
    """Capitalize column names of the model's input dataframe.

    Keep column names consistent with the dataframe used for
    training the model."""
    dataframe.columns = [x.upper() for x in dataframe.columns]
    cols = []
    for col in dataframe.columns:
        if col.endswith('_ACTIVE'):
            col = col.replace('_ACTIVE_ACTIVE', '_ACTIVE_Active')
        elif col.endswith('_CLOSED'):
            col = col.replace('_CLOSED', '_Closed')
        cols.append(col)
    dataframe.columns = cols
    return dataframe


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
        data = capitalize_column_names(data)
        data.set_index('SK_ID_CURR', inplace=True)
        data = data[ORDERED_COLS]
        data['AMT_CREDIT'] = amt
        data['AMT_ANNUITY'] = amt_annuity
        prob = infer(data)
        res = dict()
        res['input data'] = data
        res['Model response'] = (1 - prob) * 100
        return Response(res)


class ApplicationViewSet(viewsets.ModelViewSet):
    """End point for application management."""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ApplicationFilter

    @action(detail=False, methods=['GET'])
    def last_record(self, request):
        last_rec = Application.objects.order_by('pk').last()
        serializer = self.get_serializer(last_rec)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def first_record(self, request):
        first_rec = Application.objects.order_by('pk').first()
        serializer = self.get_serializer(first_rec)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def predict(self, request, pk=None):
        app = Application.objects.get(pk=pk)
        data = pd.DataFrame.from_records([model_to_dict(app)])
        data = capitalize_column_names(data)
        data.drop(columns='SK_ID_CURR', inplace=True)
        data = data[ORDERED_COLS]
        prob = infer(data)
        return Response({'Model response': (1 - prob) * 100})


class ModelExplainer(APIView):
    """Endpoint for prediction.

    receive data from POST and return refund probability.
    """
    serializer_class = PredictionSerializer

    def post(self, request, sample_size=100):
        data = PredictionSerializer(data=request.data)
        data.is_valid()
        sk_id_curr = data.data['sk_id_curr']
        amt = data.data['amt_credit']
        amt_annuity = data.data['amt_annuity']
        app = get_object_or_404(Application, pk=sk_id_curr)
        data = pd.DataFrame.from_records([model_to_dict(app)])
        data = capitalize_column_names(data)
        data.set_index('SK_ID_CURR', inplace=True)
        data = data[ORDERED_COLS]
        data['AMT_CREDIT'] = amt
        data['AMT_ANNUITY'] = amt_annuity
        res = dict()
        res['input data'] = data
        first_rec = Application.objects.order_by('pk').first().sk_id_curr
        last_rec = Application.objects.order_by('-pk').first().sk_id_curr
        sample = list()
        while len(sample) < sample_size:
            try:
                random_index = randint(first_rec, last_rec)
                random_record = Application.objects.get(pk=random_index)
                sample.append(model_to_dict(random_record))
            except ObjectDoesNotExist as e:
                pass
        sample.append(model_to_dict(app))
        sample = pd.DataFrame(sample)
        sample = capitalize_column_names(sample)
        sample.drop(columns='SK_ID_CURR', inplace=True)
        sample = sample[ORDERED_COLS]
        sample_pp, pp, m = infer(sample, transform_only=True)
        feature_names = list(pp.named_transformers_['occupation']\
                                .get_feature_names())
        feature_names = [x[3:] for x in feature_names]
        feature_names += list(sample.columns)
        feature_names.remove('OCCUPATION_TYPE')
        explainer = shap.TreeExplainer(m, data=sample_pp,
                                       model_output='probability')
        shap_values = explainer.shap_values(sample_pp)
        res['base_value'] = explainer.expected_value
        res['contribs'] = {x: y for x, y in zip(feature_names,
                                                shap_values[-1, :])}
        return Response(res)

import pickle
import os
import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from default_risk_API.settings import BASE_DIR
from api.serializers import PredictionSerializer
# Create your views here.

class Predict(APIView):
    """Endpoint for prediction.

    receive data from POST and return refund probability.
    """
    serializer_class = PredictionSerializer

    def post(self, request):
        with open(os.path.join(BASE_DIR, 'models', 'model.pickle'), 'rb') as f:
            m = pickle.load(f)
        data = PredictionSerializer(data=request.data)
        data.is_valid()
        sk_id_curr = data.data['app_id']
        amt = data.data['amt']
        amt_annuity = data.data['amt_annuity']
        data = pd.read_csv(os.path.join(BASE_DIR, 'models', 'test.csv'))
        data.set_index('SK_ID_CURR', inplace=True)
        res = {"score": (1 - m.predict(data.loc[sk_id_curr])[0]) * 100}
        return Response(res)


class Application(APIView):
    """Endpoint for application.

    return data relative to an application.
    """
    def get(self, request, pk):
        app_data = pd.read_csv(os.path.join(BASE_DIR, 'models', 'test.csv'))
        app_data.set_index('SK_ID_CURR', inplace=True)
        return Response(app_data.loc[pk].to_dict())

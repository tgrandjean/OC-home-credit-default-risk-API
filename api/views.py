import pickle
import os
import pandas as pd

from default_risk_API.settings import BASE_DIR
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['POST'])
def predict(request):
    with open(os.path.join(BASE_DIR, 'models', 'model.pickle'), 'rb') as f:
        m = pickle.load(f)
    data = request.data
    sk_id_curr = data['app_id']
    amt = data['amt']
    amt_annuity = data['amt_annuity']
    data = pd.read_csv(os.path.join(BASE_DIR, 'models', 'test.csv'))
    data.set_index('SK_ID_CURR', inplace=True)
    res = {"score": (1 - m.predict(data.loc[sk_id_curr])[0]) * 100}
    return Response(res)

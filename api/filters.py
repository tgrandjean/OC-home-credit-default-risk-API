from django_filters import rest_framework as filters
from api.models import Application


class ApplicationFilter(filters.FilterSet):
    min_sk_id_curr = filters.NumberFilter(field_name='sk_id_curr',
                                          lookup_expr='gte')
    max_sk_id_curr = filters.NumberFilter(field_name='sk_id_curr',
                                          lookup_expr='lte')
    min_days_birth = filters.NumberFilter(field_name='days_birth',
                                          lookup_expr='gte')
    max_days_birth = filters.NumberFilter(field_name='days_birth',
                                          lookup_expr='gte')
    class Meta:
        model = Application
        fields = ['min_sk_id_curr', 'max_sk_id_curr',
                  'min_days_birth', 'max_days_birth',
                  'occupation_type', 'name_contract_type'
                  ]

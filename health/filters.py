import django_filters
from .models import HealthRecord


class HealthRecordFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = HealthRecord
        fields = ['record_type', 'cat', 'is_completed']

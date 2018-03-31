from django_filters import rest_framework as filters

from todos.models import Todo


class TodoFilterSet(filters.FilterSet):

    due_date_before = filters.DateFilter(name='due_date__date', lookup_expr='lte')
    has_completed = filters.BooleanFilter(name='has_completed')

    class Meta:
        model = Todo
        fields = [
            'due_date_before',
            'has_completed',
        ]

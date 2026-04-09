import django_filters

from .models import Task, Project


class TaskFilter(django_filters.FilterSet):
    """Класс фильтрации по дате """
    due_date_before = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    due_date_after = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')

    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all())


    class Meta:
        model = Task
        fields = ['status', 'priority', 'project']

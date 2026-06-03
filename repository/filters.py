import django_filters
from .models import Publication, Dataset, UserProfile

class PublicationFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    journal_name = django_filters.CharFilter(lookup_expr='icontains', label='Journal')
    status = django_filters.ChoiceFilter(choices=Publication.STATUS_CHOICES)

    class Meta:
        model = Publication
        fields = ['title', 'journal_name', 'status']

class DatasetFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Dataset Title')

    class Meta:
        model = Dataset
        fields = ['title']

class ResearcherFilter(django_filters.FilterSet):
    user__first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    user__last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last Name')
    department = django_filters.CharFilter(lookup_expr='icontains', label='Department')

    class Meta:
        model = UserProfile
        fields = ['user__first_name', 'user__last_name', 'department']
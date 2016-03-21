# -*- coding: utf-8 -*-
from dal import autocomplete

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .models import Entry
urlpatterns = [
    # URL pattern for the UserListView
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=Entry,
            create_field='value',
        ),
        name='select2_many_to_many_autocomplete',
    ),
]

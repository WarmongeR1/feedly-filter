# -*- coding: utf-8 -*-
from dal import autocomplete
from django.conf.urls import *

from .models import Entry
from .views import CollectionListView, CollectionDetailView

urlpatterns = [

    url(r'^$', CollectionListView.as_view(), name='collection-list'),
    url(r'^(?P<pk>[-\w]+)/$', CollectionDetailView.as_view(), name='collection-detail'),

    url(
        'other/entry-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=Entry,
            create_field='value',
        ),
        name='select2_many_to_many_autocomplete',
    ),
]

# -*- coding: utf-8 -*-
from dal import autocomplete
from django.conf.urls import *

from .models import Entry
from .views import CollectionListView, CollectionDetailView, ajax_user_subscribe_collection, ajax_user_unsubscribe_collection

urlpatterns = [

    url(r'^$', CollectionListView.as_view(), name='collection-list'),
    url(r'^(?P<pk>[-\w]+)/$', CollectionDetailView.as_view(), name='collection-detail'),

    url(r'^ajax/subscribe', ajax_user_subscribe_collection, name='collection-subscribe'),
    url(r'^ajax/unsubscribe', ajax_user_unsubscribe_collection, name='collection-unsubscribe'),

    url(
        'other/entry-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=Entry,
            create_field='value',
        ),
        name='select2_many_to_many_autocomplete',
    ),
]

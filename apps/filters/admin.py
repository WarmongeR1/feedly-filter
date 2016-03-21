# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dal import autocomplete
from django import forms
from django.contrib import admin

from .models import Entry, Collection, Category, UserCollection


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        widgets = {
            'category': autocomplete.ModelSelect2Multiple(
                'filters:select2_many_to_many_autocomplete'
            )
        }


class EntryAdmin(admin.ModelAdmin):
    form = EntryForm


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'
        widgets = {
            'entries': autocomplete.ModelSelect2Multiple(
                'filters:select2_many_to_many_autocomplete'
            )
        }


class CollectionAdmin(admin.ModelAdmin):
    form = CollectionForm


admin.site.register(Entry, EntryAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Category)
admin.site.register(UserCollection)

# -*- encoding: utf-8 -*-
import csv

from allauth.socialaccount.models import SocialToken
from django.core.management.base import BaseCommand

from apps.filters.filter import get_api
import os
from django.conf import settings
from yaml import load

from apps.filters.models import Collection, Entry, Category


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        folder = settings.APPS_DIR.path('filters', 'data').root

        config_path = os.path.join(folder, 'collections.yaml')

        assert os.path.exists(config_path)

        with open(config_path, 'r') as fio:
            config = load(fio.read())

        for item in config:
            collection, _ = Collection.objects.get_or_create(
                title=item['name'],
            )

            if not collection.description:
                collection.description = item['description']
                collection.save()

            with open(os.path.join(folder, item['file']), 'r') as fio:
                reader = csv.DictReader(fio)
                for i, row in enumerate(reader):
                    categories = []
                    for category in row['category'].split(','):
                        categories.append(Category.objects.get_or_create(title=category.strip())[0])

                    entry, _ = Entry.objects.get_or_create(value=row['value'], type=row['type'])
                    entry.category.add(*categories)
                    collection.entries.add(entry)

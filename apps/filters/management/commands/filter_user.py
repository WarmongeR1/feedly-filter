# -*- encoding: utf-8 -*-


from django.core.management.base import BaseCommand

from apps.filters.filter import main


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        main()

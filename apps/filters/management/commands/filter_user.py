# -*- encoding: utf-8 -*-


from django.core.management.base import BaseCommand

from apps.filters.filter import filter_user
from apps.users.models import User


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        filter_user(User.objects.get(id=options['user_id']))

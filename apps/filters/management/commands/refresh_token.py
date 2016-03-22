# -*- encoding: utf-8 -*-
from allauth.socialaccount.models import SocialToken
from django.core.management.base import BaseCommand

from apps.filters.filter import get_api


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        tokens = SocialToken.objects.filter(account__user__id=options['user_id'], account__provider='feedly')
        for item in tokens:
            item.token = get_api().refresh_access_token(item.token_secret).get('access_token')
            item.save()

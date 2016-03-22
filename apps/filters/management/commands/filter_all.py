# -*- encoding: utf-8 -*-
from allauth.socialaccount.models import SocialToken
from django.core.management.base import BaseCommand
from django_q.tasks import async

from apps.filters.filter import filter_user
from apps.users.models import User


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        users = User.objects.filter(id__in=SocialToken.objects.all().values_list('account__user', flat=True))

        for user in users:
            async(filter_user, user)

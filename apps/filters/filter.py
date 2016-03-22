# -*- encoding: utf-8 -*-

import lxml.html as lh
from allauth.socialaccount.models import SocialToken, SocialApp
from django.conf import settings
from feedly.client import FeedlyClient

from apps.users.models import User
from .models import UserCollection, Entry


def get_api(token=None):
    conf = SocialApp.objects.get(provider='feedly')

    options = dict(
        client_id=conf.client_id,
        client_secret=conf.secret,
        sandbox=settings.SOCIALACCOUNT_PROVIDERS['feedly']['FEEDLY_HOST'] == 'sandbox.feedly.com'
    )
    if token is not None:
        options['token'] = token,

    return FeedlyClient(**options)


def get_categories(api):
    return api.get_info_type(api.token, 'categories')


def mark_read(api, ids):
    if ids:
        api.mark_article_read(api.token, ids)


def filter_articles(articles, filters) -> list:
    mark_ids = []
    for item in articles:
        try:
            # url = item.get('alternate')[0].get('href')
            title = item.get('title', '')
            description = item.get('summary', {}).get('content')
            if description is None:
                description = ''
            else:
                description = lh.fromstring(description).text_content().strip()
        except TypeError as e:
            # print(e, description, title)
            pass
        else:
            for filter in filters:
                if filter.filter(description) or filter.filter(title):
                    mark_ids.append(item['id'])
                    print(title)

    return mark_ids


def get_articles(api) -> list:
    result = []

    for i, category in enumerate(get_categories(api)):
        data = api.get_feed_content(api.token, category.get('id'), True, 1457330281)
        items = data.get('items', [])
        result.extend(items)

    return result


def get_feedly_token(user):
    return SocialToken.objects.filter(account__user=user, account__provider='feedly')


def filter_user(user: User):
    tokens = get_feedly_token(user)

    if tokens:
        token = tokens[0].token
        api = get_api(token)

        mark_read(api,
                  filter_articles(
                      get_articles(api),
                      Entry.objects.filter(id__in=UserCollection.objects.filter(user=user).values_list(
                          'collection__entries__pk', flat=True))))

import re
from functools import partial

from django.db import models
from django.utils.translation import ugettext as _

from apps.users.models import User

TYPE_CHOICES = (
    (1, 'word (nocase)'),
    (2, 'word (case)'),
    (3, 'regex'),
)


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'), unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.title


class Entry(models.Model):
    value = models.CharField(max_length=255, verbose_name=_('Value'), unique=True)
    category = models.ManyToManyField(Category, verbose_name=_('Category'))  # sphere, tags
    type = models.IntegerField(choices=TYPE_CHOICES)

    def _no_case_check(self, text):
        return text and self.value and self.value.lower() in text.lower()

    def _case_check(self, text):
        return text and self.value and self.value in text

    def _regex_check(self, text):
        return text and self.value and bool(re.search(self.value, text))

    def _true_check(self, text):
        return True

    checkers = {
        1: _no_case_check,
        2: _case_check,
        3: _regex_check,
    }

    def filter(self, text):
        return self.checkers.get(self.type, self._true_check)(self=self, text=text)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.value


class Collection(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'), unique=True)
    description = models.TextField(verbose_name=_('Description'), default='None')
    entries = models.ManyToManyField(Entry)

    def __str__(self):
        return self.title


class UserCollection(models.Model):
    collection = models.ForeignKey(Collection)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('collection', 'user')

    def __str__(self):
        return "{} - {}".format(self.collection.title, self.user.username)

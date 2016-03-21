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

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.value


class Collection(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'), unique=True)
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

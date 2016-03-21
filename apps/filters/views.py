# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Collection


class CollectionListView(ListView):
    model = Collection


class CollectionDetailView(DetailView):
    model = Collection

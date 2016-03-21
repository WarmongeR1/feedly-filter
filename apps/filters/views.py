# Create your views here.

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django_ajax.decorators import ajax

from .models import Collection, UserCollection


class CollectionListView(ListView):
    model = Collection

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        if self.request.user and not self.request.user.is_anonymous():
            context['collections'] = UserCollection.objects.filter(user=self.request.user).values_list('collection__pk',
                                                                                                       flat=True)
        return context


class CollectionDetailView(DetailView):
    model = Collection


@ajax
@login_required
def ajax_user_subscribe_collection(request):
    try:
        UserCollection.objects.get_or_create(user=request.user,
                                             collection=Collection.objects.get(pk=request.POST.get('collection')))
    except Exception as e:
        return {'ok': False, 'error': str(e)}
    else:
        return {'ok': True}


@ajax
@login_required
def ajax_user_unsubscribe_collection(request):
    try:
        subscribtions = UserCollection.objects.filter(user=request.user,
                                                      collection=Collection.objects.get(
                                                          pk=request.POST.get('collection')))
        if subscribtions and subscribtions.count() > 0:
            subscribtions.delete()
    except Exception as e:
        return {'ok': False, 'error': str(e)}
    else:
        return {'ok': True}

from django.shortcuts import render
from social.models import User as OurUser


def profile_view(request):
    context = {}

    login = request.GET.get('user', request.user.username)
    user = OurUser.objects.filter(name=login).first()
    context['user'] = user
    if 'HX-Request' in request.headers:
        return render(request, 'components/profile.html', context)
    else:
        return render(request, 'components/profile_full.html', context)
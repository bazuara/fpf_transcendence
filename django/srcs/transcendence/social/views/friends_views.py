from django.shortcuts import render, redirect, get_object_or_404
from social.models import User as OurUser

def friends_view(request, name):
    profile_user = get_object_or_404(OurUser, name=name)

    authenticated_user = request.user

    friend_list = profile_user.friends.all()

    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user,   # DjangoUser instance
        'error_msg'         : None,
        'friend_list'       : friend_list,
    }

    if 'HX-Request' in request.headers:
        return render(request, 'friends/friends.html', context)
    else:
        return render(request, 'friends/friends_full.html', context)


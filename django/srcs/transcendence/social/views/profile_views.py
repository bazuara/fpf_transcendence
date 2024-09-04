from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from social.forms import ChangeAliasForm, ChangeAvatarForm
from social.models import User as OurUser

def profile_view(request, name):
    # Fetch OurUser from social.models
    profile_user = get_object_or_404(OurUser, name=name)

    # Get the authenticated user from the request (session user)
    authenticated_user = request.user
    
    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user    # DjangoUser instance
    }

    # Return different templates based on whether it's an HTMX request
    if 'HX-Request' in request.headers:
        return render(request, 'social_template_full.html', context)
    else:
        return render(request, 'social_template_full_full.html', context)

def change_alias(request, name):
    profile_user = get_object_or_404(OurUser, name=name)

    authenticated_user = request.user
    
    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user,   # DjangoUser instance
        'error_msg'         : None,
    }

    # Ensure the logged-in user can only change their own alias
    if authenticated_user.username != profile_user.name:
        context['error_msg'] = "You are not allowed to change this user's alias."
        if 'HX-Request' in request.headers:
            return render(request, 'social_template_full.html', context)
        else:
            return render(request, 'social_template_full_full.html', context)

    if request.method == 'POST':
        form = ChangeAliasForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            if 'HX-Request' in request.headers:
                return render(request, 'social_template_full.html', context)
            else:
                return render(request, 'social_template_full_full.html', context)
    else:
        form = ChangeAliasForm(instance=profile_user)

    context['form'] = form
    if 'HX-Request' in request.headers:
        return render(request, 'alias/change_alias.html', context)
    else:
        return render(request, 'alias/change_alias_full_full.html', context)


def change_avatar(request, name):
    profile_user = get_object_or_404(OurUser, name=name)

    authenticated_user = request.user
    
    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user,   # DjangoUser instance
        'error_msg'         : None,
    }

    # Ensure the logged-in user can only change their own avatar
    if authenticated_user.username != profile_user.name:
        context['error_msg'] = "You are not allowed to change this user's avatar."
        if 'HX-Request' in request.headers:
            return render(request, 'social_template_full.html', context)
        else:
            return render(request, 'social_template_full_full.html', context)
    
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()
            if 'HX-Request' in request.headers:
                return render(request, 'social_template_full.html', context)
            else:
                return render(request, 'social_template_full_full.html', context)
    else:
        form = ChangeAvatarForm(instance=profile_user)

    context['form'] = form
    if 'HX-Request' in request.headers:
        return render(request, 'avatar/change_avatar.html', context)
    else:
        return render(request, 'avatar/change_avatar_full_full.html', context)


def game_history_view(request, name):
    profile_user = get_object_or_404(OurUser, name=name)

    authenticated_user = request.user

    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user,   # DjangoUser instance
        'error_msg'         : None,
    }

    if 'HX-Request' in request.headers:
        return render(request, 'game_history/game_history.html', context)
    else:
        return render(request, 'social_template_full_full.html', context)


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
        return render(request, 'friends/friends_full_full.html', context)

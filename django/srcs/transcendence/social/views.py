import os

from django.contrib.auth import logout
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from social.forms import ChangeAliasForm, ChangeAvatarForm, ManageFriendsForm
from social.models import User as OurUser
from social.anonymization import clear_user_data
from game.models import Game

def get_user_games(profile_user):
    return Game.objects.filter(
        Q(user1=profile_user) |
        Q(user2=profile_user) |
        Q(user3=profile_user) |
        Q(user4=profile_user)
        ).exclude(game_mode="T")

def social_view(request, name):
    # Fetch OurUser from social.models
    profile_user = get_object_or_404(OurUser, name=name)

    # Get the authenticated user from the request (session user)
    authenticated_user = request.user
    
    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user    # DjangoUser instance
    }

    games = get_user_games(profile_user)

    context['games1v1'] = games.filter(user2=None)
    context['games2v2'] = games.exclude(user2=None)

    # Return different templates based on whether it's an HTMX request
    if 'HX-Request' in request.headers:
        return render(request, 'social_template_full.html', context)
    else:
        return render(request, 'social_template_full_full.html', context)

def profile_view(request, name):
    profile_user = get_object_or_404(OurUser, name=name)

    authenticated_user = request.user
    
    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user,   # DjangoUser instance
    }

    if not 'HX-Request' in request.headers:
        games = get_user_games(profile_user)

        context['games1v1'] = games.filter(user2=None)
        context['games2v2'] = games.exclude(user2=None)
    
    if 'HX-Request' in request.headers:
        return render(request, 'profile/profile_info.html', context)
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

    if not 'HX-Request' in request.headers:
        games = get_user_games(profile_user)

        context['games1v1'] = games.filter(user2=None)
        context['games2v2'] = games.exclude(user2=None)

    # Ensure the logged-in user can only change their own alias
    if authenticated_user.username != profile_user.name:
        context['error_msg'] = "You are not allowed to change this user's alias."
        if 'HX-Request' in request.headers:
            return render(request, 'profile/profile_info.html', context)
        else:
            return render(request, 'social_template_full_full.html', context)

    if request.method == 'POST':
        form = ChangeAliasForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            if 'HX-Request' in request.headers:
                 return render(request, 'profile/profile_info.html', context)
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

    if not 'HX-Request' in request.headers:
        games = get_user_games(profile_user)

        context['games1v1'] = games.filter(user2=None)
        context['games2v2'] = games.exclude(user2=None)

    if authenticated_user.username != profile_user.name:
        context['error_msg'] = "You are not allowed to change this user's avatar."
        if 'HX-Request' in request.headers:
            return render(request, 'profile/profile_info.html', context)
        else:
            return render(request, 'social_template_full_full.html', context)
    
    if request.method == 'POST':
        if profile_user.avatar:
            old_avatar = profile_user.avatar.path
        else:
            old_avatar = None
        form = ChangeAvatarForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            if old_avatar and os.path.exists(old_avatar):
                os.remove(old_avatar)
            form.save()
            if not form.files:
                profile_user.avatar = None
                profile_user.save()
            if 'HX-Request' in request.headers:
                return render(request, 'profile/profile_info.html', context)
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
    }

    games = get_user_games(profile_user)

    context['games1v1'] = games.filter(user2=None)
    context['games2v2'] = games.exclude(user2=None)

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
        'friend_list'       : friend_list,
        'error_msg'         : None,
    }

    try:
        if request.method == 'POST':
            form = ManageFriendsForm(request.POST, instance=profile_user)
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'add':
                    new_friend_name = request.POST.get('new_friend_name')
                    if not new_friend_name:
                        raise ValueError("Empty user")
                    new_friend_name = str(new_friend_name).lower().strip()
                    new_friend = OurUser.objects.filter(name=new_friend_name).first()
                    if not new_friend:
                        raise ValueError(f"User {new_friend_name} not found.")
                    if new_friend == profile_user:
                        raise ValueError("You cannot add yourself as a friend.")
                    profile_user.friends.add(new_friend)
                elif action == 'delete':
                    friend_id = request.POST.get('user_id')
                    friend = get_object_or_404(OurUser, id=friend_id)
                    profile_user.friends.remove(friend)
    except Exception as e:
        context['error_msg'] = str(e)

    if 'HX-Request' in request.headers:
        return render(request, 'friends/friends.html', context)
    else:
        return render(request, 'friends/friends_full_full.html', context)


def anonymize_view(request, name):
    profile_user = get_object_or_404(OurUser, name=name)
    authenticated_user = request.user

    context = {
        'profile_user'      : profile_user,         # OurUser instance
        'authenticated_user': authenticated_user,   # DjangoUser instance
        'error_msg' : None,
    }

    if profile_user.name != authenticated_user.username:
        context['error_msg'] = "Unauthorized: You can only delete your own profile."
        return render(request, 'friends/friends_full_full.html', context)

    clear_user_data(profile_user)
    logout(request)
    return redirect('landing')

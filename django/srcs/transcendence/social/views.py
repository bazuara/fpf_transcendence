import random, string
from django.contrib.auth import logout
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from social.forms import ChangeAliasForm, ChangeAvatarForm, ManageFriendsForm
from social.models import User as OurUser
from game.models import Game

def get_user_games(profile_user):
    return Game.objects.filter(
        Q(user1=profile_user) |
        Q(user2=profile_user) |
        Q(user3=profile_user) |
        Q(user4=profile_user)
        )

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

    context['games1v1'] = games.filter(user2__isnull=True)
    context['games2v2'] = games.filter(user2__isnull=False)

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

        context['games1v1'] = games.filter(user2__isnull=True)
        context['games2v2'] = games.filter(user2__isnull=False)
    
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

        context['games1v1'] = games.filter(user2__isnull=True)
        context['games2v2'] = games.filter(user2__isnull=False)

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

        context['games1v1'] = games.filter(user2__isnull=True)
        context['games2v2'] = games.filter(user2__isnull=False)

    if authenticated_user.username != profile_user.name:
        context['error_msg'] = "You are not allowed to change this user's avatar."
        if 'HX-Request' in request.headers:
            return render(request, 'profile/profile_info.html', context)
        else:
            return render(request, 'social_template_full_full.html', context)
    
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()
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

    context['games1v1'] = games.filter(user2__isnull=True)
    context['games2v2'] = games.filter(user2__isnull=False)

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
    def generate_random_string_with_uppercase():
        uppercase_letter = random.choice(string.ascii_uppercase)
        remaining_characters = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        random_position = random.randint(0, 9)
        random_text = remaining_characters[:random_position] + uppercase_letter + remaining_characters[random_position:]
        return random_text

    def gen_random_name():
        random_text = generate_random_string_with_uppercase()
        user = OurUser.objects.filter(name=random_text).first()
        if not user:
            return random_text
        else:
            gen_random_name()

    def clear_user_data(user):
        new_name = gen_random_name()
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
        user.intra_image = None
        user.name = new_name
        user.alias = new_name

        users_with_user_as_friend = OurUser.objects.filter(friends=user)
        for foreign_user in users_with_user_as_friend:
            foreign_user.friends.remove(user)
        user.friends.clear()
        user.save()

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

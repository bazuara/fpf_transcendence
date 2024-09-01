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
        return render(request, 'profile/profile.html', context)
    else:
        return render(request, 'profile/profile_full.html', context)

def change_alias(request, name):
    profile_user = get_object_or_404(OurUser, name=name)

    # Ensure the logged-in user can only change their own alias
    if request.user.username != profile_user.name:
        return HttpResponseForbidden("You are not allowed to change this user's alias.")

    if request.method == 'POST':
        form = ChangeAliasForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect('profile', name=profile_user.name)
    else:
        form = ChangeAliasForm(instance=profile_user)

    return render(request, 'profile/components/change_alias.html', {'form': form, 'user': profile_user})

def change_avatar(request, name):
    profile_user = get_object_or_404(OurUser, name=name)
    
    # Ensure the logged-in user can only change their own avatar
    if request.user.username != profile_user.name:
        return HttpResponseForbidden("You are not allowed to change this user's avatar.")
    
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect('profile', name=profile_user.name)
    else:
        form = ChangeAvatarForm(instance=profile_user)
    
    return render(request, 'profile/components/change_avatar.html', {'form': form, 'user': profile_user})

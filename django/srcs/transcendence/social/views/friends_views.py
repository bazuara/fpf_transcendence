from django.shortcuts import render

def friends_view(request):
    context = {
        'title' : "friends",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'friends/friends.html')
    else:
        return render(request, 'friends/friends_full.html', context)

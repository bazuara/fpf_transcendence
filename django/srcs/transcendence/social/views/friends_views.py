from django.shortcuts import render

def friends_view(request):
    context = {
        'title' : "friends",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/friends.html')
    else:
        return render(request, 'components/friends_full.html', context)
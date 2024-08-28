from django.shortcuts import render

def profile_view(request):
    context = {
        'title' : "profile",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/profile.html')
    else:
        return render(request, 'components/profile_full.html', context)

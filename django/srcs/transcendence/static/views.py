from django.shortcuts import render

def welcome_view(request):
    context = {
        'title' : "welcome",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/welcome.html')
    else:
        return render(request, 'components/welcome_full.html', context)

def about_view(request):
    context = {
        'title' : "about",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/about.html')
    else:
        return render(request, 'components/about_full.html', context)

def how_to_play_view(request):
    context = {
        'title' : "how_to_play",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/how_to_play.html')
    else:
        return render(request, 'components/how_to_play_full.html', context)


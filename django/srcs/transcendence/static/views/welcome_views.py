from django.shortcuts import render

def welcome_view(request):
    context = {
        'title' : "welcome",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/welcome.html')
    else:
        return render(request, 'components/welcome_full.html', context)
    

def base_view(request):
    return render(request, 'base.html')

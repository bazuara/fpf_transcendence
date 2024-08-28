from django.shortcuts import render

def about_view(request):
    context = {
        'title' : "About",
    }
    if 'HX-Request' in request.headers:
        return render(request, 'components/about.html')
    else:
        return render(request, 'components/about_full.html', context)

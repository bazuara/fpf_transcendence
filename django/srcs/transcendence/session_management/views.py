from django.shortcuts import render

def login_view(request):
    context = {
        'Title' : "Trancendence",
    }
    return render(request, 'login.html', context)

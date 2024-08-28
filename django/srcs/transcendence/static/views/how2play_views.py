from django.shortcuts import render

def how2play_view(request):
    context = {
        'Title' : "Trancendence",
    }
    return render(request, 'index.html', context)
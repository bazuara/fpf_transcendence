from django.shortcuts import render

def index_view(request):
    context = {
        'title' : "Index.html",
    }
    return render(request, 'index.html', context)
from django.shortcuts import render

def rooms_view(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms.html')
    else:
        return render(request, 'rooms/rooms_full.html')

def rooms_create(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_create.html')
    else:
        return render(request, 'rooms/rooms_create_full.html')
    
def rooms_join(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join.html')
    else:
        return render(request, 'rooms/rooms_join_full.html')
    
def rooms_join_public(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_public.html')
    else:
        return render(request, 'rooms/rooms_join_public_full.html')
    
def rooms_join_private(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_private.html')
    else:
        return render(request, 'rooms/rooms_join_private_full.html')
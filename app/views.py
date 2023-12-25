# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PublicChatRoom, PublicRoomChatMessage
from django.utils import timezone

def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    user = request.user
    chat_room, created = PublicChatRoom.objects.get_or_create(title='Django')
    
    # if the user is not already in the chat room then add them
    if user not in chat_room.users.all():
        chat_room.users.add(user)

    # get all messages for the current chat room, ordered by timestamp
    messages = PublicRoomChatMessage.objects.filter(room=chat_room).order_by('-timestamp')

    if request.method == 'POST':
        message_content = request.POST.get('message', '')
        if message_content:
            #new message for the current user and chat room
            PublicRoomChatMessage.objects.create(
                user=user,
                room=chat_room,
                timestamp=timezone.now(),
                content=message_content
            )
            return redirect('home')

    return render(request, 'home.html', {'user': user, 'messages': messages})

def redirect_to_chat_room(request):
    return redirect('home')

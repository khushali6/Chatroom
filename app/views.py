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

    # Get the chat room or create it if it doesn't exist (for simplicity, we'll use a fixed title)
    chat_room, created = PublicChatRoom.objects.get_or_create(title='Django')
    
    # If the user is not already in the chat room, add them
    if user not in chat_room.users.all():
        chat_room.users.add(user)

    # Get all messages for the current chat room, ordered by timestamp (latest first)
    messages = PublicRoomChatMessage.objects.filter(room=chat_room).order_by('-timestamp')

    if request.method == 'POST':
        message_content = request.POST.get('message', '')
        if message_content:
            # Create a new message for the current user and chat room
            PublicRoomChatMessage.objects.create(
                user=user,
                room=chat_room,
                timestamp=timezone.now(),
                content=message_content
            )

            # Redirect to the same chat room page to avoid form resubmission on page refresh
            return redirect('home')

    return render(request, 'home.html', {'user': user, 'messages': messages})

def redirect_to_chat_room(request):
    # Redirect to the chat room (for simplicity, we'll use a fixed title)
    return redirect('home')

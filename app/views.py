# app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PublicChatRoom, PublicRoomChatMessage
from django.utils import timezone

def login(request):
    
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from app.models import PublicChatRoom, PublicRoomChatMessage

@login_required
def home(request):
    # Get or create the chat room titled "Django"
    chat_room_title = "Django"
    user = request.user

    # Get the chat room or create it if it doesn't exist
    chat_room, created = PublicChatRoom.objects.get_or_create(title=chat_room_title)
    
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

            # Redirect to the home page to avoid form resubmission on page refresh
            return redirect('home')

    return render(request, 'home.html', {'user': user, 'chat_room_title': chat_room_title, 'messages': messages})

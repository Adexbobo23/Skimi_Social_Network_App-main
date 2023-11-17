from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Chat
from django.db.models import Q
from friend.models import FriendList
from django.contrib.auth.models import User
from users.models import Profile
from random import sample
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import ChatHistory
from django.contrib.auth.models import User
from random import sample
import openai
from django.conf import settings

@login_required(login_url='login')
def room_enroll(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    friends = FriendList.objects.filter(user=request.user)[0].friends.all()
    all_rooms = Room.objects.filter(
        Q(author=request.user) | Q(friend=request.user)
    ).order_by('-created')

    context = {
        'all_rooms':all_rooms,
        'all_friends':friends,
        'random_users':random_users, 
        'user_profile': user_profile
    }
    return render(request, 'chat/join_room.html', context)



@login_required(login_url='login')
def room_choice(request, friend_id):
    friend = User.objects.filter(pk=friend_id)
    if not friend:
        messages.error(request, 'Invalid User ID')
        return redirect('room-enroll') 
    if not FriendList.objects.filter(user=request.user, friends=friend[0]):
        messages.error(request, 'You need to be friends to chat')
        return redirect('room-enroll') 

    room = Room.objects.filter(
        Q(author=request.user, friend=friend[0]) | Q(author=friend[0], friend=request.user)
    )
    if not room:
        create_room = Room(author=request.user, friend=friend[0])
        create_room.save()
        room = create_room.room_id
        return redirect('room', room, friend_id)

    return redirect('room', room[0].room_id, friend_id)


""" Chatroom between users """
@login_required(login_url='login')
def room(request, room_name, friend_id):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    all_rooms = Room.objects.filter(room_id=room_name)
    if not all_rooms:  
        messages.error(request, 'Invalid Room ID')
        return redirect('room-enroll')

    chats = Chat.objects.filter(
        room_id=room_name
    ).order_by('date')

    context = {
        'old_chats':chats,
        'my_name':request.user,
        'friend_name':User.objects.get(pk=friend_id),
        'room_name': room_name,
        'random_users':random_users,
        'user_profile': user_profile
    }
    return render(request, 'chat/chatroom.html', context)


@login_required(login_url='login')
def chat_skimi(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    friends = FriendList.objects.filter(user=request.user)[0].friends.all()
    all_rooms = Room.objects.filter(
        Q(author=request.user) | Q(friend=request.user)
    ).order_by('-created')

    context = {
        'all_rooms':all_rooms,
        'all_friends':friends,
        'random_users':random_users,
        'user_profile': user_profile
    }

    return render(request, 'chat/index.html', context)


import openai

from django.http import JsonResponse

class ChatBotView(View):
    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None

        users = list(User.objects.exclude(pk=request.user.pk))
        cnt = min(5, len(users))
        random_users = sample(users, cnt)

        context = {
            'random_users': random_users,
            'user_profile': user_profile
        }

        return render(request, 'chat/chat-bot-s2.html', context)

    def post(self, request):
        prompt = request.POST.get('prompt')

        user = request.user 

        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=50,
            )

            chat_entry = ChatHistory(user=user, input_message=prompt, bot_response=response.choices[0].text)
            chat_entry.save()

            return JsonResponse({'response': response.choices[0].text})
        except Exception as e:
            # Log the error for debugging
            print("Error:", e)
            return JsonResponse({'error': str(e)})
    
@login_required(login_url='login')
def all_friends(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    context = {
        'random_users':random_users,
        'user_profile': user_profile
    }

    return render(request, 'chat/contact.html', context)

@login_required(login_url='login')
def story(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    stories = Story.objects.all()

    context = {
        'random_users':random_users,
        'user_profile': user_profile,
        'stories': stories
    }

    return render(request, 'chat/stories.html', context)

@login_required(login_url='login')
def chatbot_welcome(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    context = {
        'random_users':random_users,
        'user_profile': user_profile
    }


    return render(request, 'chat/chat-bot-welcome.html', context)

@login_required(login_url='login')
def pricing(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    context = {
        'random_users':random_users,
        'user_profile': user_profile
    }

    return render(request, 'chat/pricing.html', context)

@login_required(login_url='login')
def faq(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    context = {
        'random_users':random_users,
        'user_profile': user_profile
    }

    return render(request, 'chat/faq.html', context)


from django.shortcuts import render, redirect
from .models import Story
from .forms import StoryForm


@login_required(login_url='login')
def add_story(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('story')
    else:
        form = StoryForm()

    context = {
        'random_users':random_users,
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'chat/add-story.html', context)

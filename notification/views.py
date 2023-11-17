from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from notification.models import Notification
from users.models import Profile
from django.contrib.auth.models import User
from random import sample

# Create your views here.nnn

""" All notifications """
@login_required
def ShowNotifications(request):

    users = list(User.objects.exclude(pk=request.user.pk))
    if len(users) > 3:
        cnt = 5
    else:
        cnt = len(users)
    random_users = sample(users, cnt)

    try:
        user_profile = Profile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    context = {
        'notifications':notifications,
        'user_profile': user_profile,
        'random_users': random_users,
    }
    return render(request, 'blog/notifications.html', context)
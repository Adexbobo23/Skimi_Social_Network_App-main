from django.urls import path
from . import views
from .views import ChatBotView

urlpatterns = [
    path('', views.room_enroll, name='room-enroll'),
    path('chat/<int:friend_id>', views.room_choice, name='room-choice'),
    path('room/<int:room_name>-<int:friend_id>', views.room, name='room'),
    path('chat-skimi/', views.chat_skimi, name='chat'),
    path('chatbot/', ChatBotView.as_view(), name='chatbot'),
    path('all-friends/', views.all_friends, name='all-friend'),
    path('stories/', views.story, name='story'),
    path('chat-welcome/', views.chatbot_welcome, name='chatbot-welcome'),
    path('pricing/', views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    path('add_story/', views.add_story, name='add_story'),
]
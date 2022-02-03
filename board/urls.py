from django.urls import path

from .views import base_views, discussion_views, answer_views, vote_views

app_name = 'board'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:discussion_id>/',
         base_views.detail, name='detail'),

    # discussion_views.py
    path('discussion/create/',
         discussion_views.discussion_create, name='discussion_create'),
    path('discussion/modify/<int:discussion_id>/',
         discussion_views.discussion_modify, name='discussion_modify'),
    path('discussion/delete/<int:discussion_id>/',
         discussion_views.discussion_delete, name='discussion_delete'),

    # answer_views.py
    path('answer/create/<int:discussion_id>/',
         answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/',
         answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',
         answer_views.answer_delete, name='answer_delete'),

    # vote_views.py
    path('vote/discussion/<int:discussion_id>/', vote_views.vote_discussion, name='vote_discussion'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),
]

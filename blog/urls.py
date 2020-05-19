from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # API to post a comment
    path('postComment', views.postComment, name='postComment'),
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),

    # path('gate/gateNote.html', views.gateNote, name='gateNote'),
    # path('gate/yearPaper.html', views.yearPaper, name='yearPaper'),
    # path('gate/year/Y_2020.html', views.Y_2020, name='Y_2020'),
    # path('gate/subPaper.html', views.subPaper, name='subPaper'),
]
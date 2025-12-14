from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='main'),
    path('pythonbasics/',views.python_basics, name='pythonbasics'),
    path('cbasics/',views.c_basics, name='cbasics'),
    path('c++basics/',views.cpp_basics, name='c++basics'),
    path('javabasics/',views.java_basics, name='javabasics'),
    path('signin/',views.signin, name='signin'),
    #path('register/',views.register, name='register'),
    path('compiler/',views.codecompiler, name='compiler'),
    path('aichatbot/',views.aichatbot, name='aichatbot'),

]

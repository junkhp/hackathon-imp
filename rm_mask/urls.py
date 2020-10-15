from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexPageView, name='index'),
    path('mask', views.MaskPageView, name='mask'),
    path('result', views.ResultPageView, name='result'),
]

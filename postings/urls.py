from django.urls import path
from . import views

app_name = 'postings'

urlpatterns = [
    path('', views.index, name='index'),
]

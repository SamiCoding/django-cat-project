from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('adventure/home/', views.adventure_home, name='adventure_home'),
    path('weapon/get/', views.weapon_get, name='weapon_get'),
    path('adventure/attack/', views.adventure_attack, name='adventure_attack'),
    path('adventure/attack/result/', views.adventure_attack_result, name='adventure_attack_result'),
    path('weapon/workroom/', views.weapon_workroom, name='weapon_workroom'),
    path('weapon/pick/', views.weapon_pick, name='weapon_pick'),
    path('weapon/change/', views.weapon_change, name='weapon_change'),
    path('weapon/upgrade/', views.weapon_upgrade, name='weapon_upgrade'),
]

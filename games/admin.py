from django.contrib import admin
from .models import Event, DefaultLuckyItem, LuckyItem, DefaultWeapon, Weapon, Character, Enemy

admin.site.register(Event)
admin.site.register(DefaultLuckyItem)
admin.site.register(LuckyItem)
admin.site.register(DefaultWeapon)
admin.site.register(Weapon)
admin.site.register(Character)
admin.site.register(Enemy)
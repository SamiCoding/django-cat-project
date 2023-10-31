from django.db import models
from django.conf import settings

class Event(models.Model):
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    def __str__(self):
        if self.active:
            return f'{self.order}. {self.title} (개최중)'
        else:
            return f'{self.order}. {self.title} (종료)'

class DefaultLuckyItem(models.Model):
    name = models.CharField(max_length=20)
    power = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, related_name='default_lucky_item_list', null=True, blank=True)
    max_level = models.IntegerField(default=3)
    def __str__(self):
        lucky_item_name = self.name
        if self.event :
            lucky_item_name += '(이벤트)'
        return f'{lucky_item_name} - 공격력:{self.power}'

class LuckyItem(models.Model):
    default_lucky_item = models.ForeignKey(DefaultLuckyItem, on_delete=models.SET_NULL, related_name='lucky_item_list', null=True, blank=True)
    power = models.IntegerField()
    level = models.IntegerField(default=1)
    def __str__(self):
        return f'{self.default_lucky_item.name}.LV{self.level}'

class DefaultWeapon(models.Model):
    name = models.CharField(max_length=20)
    power = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, related_name='default_weapon_list', null=True, blank=True)
    def __str__(self):
        weapon_name = self.name
        if self.event :
            weapon_name += '(이벤트)'
        return f'{weapon_name} - 공격력:{self.power}'

class Weapon(models.Model):
    default_weapon = models.ForeignKey(DefaultWeapon, on_delete=models.SET_NULL, related_name='weapon_list', null=True, blank=True)
    power = models.IntegerField()
    level = models.IntegerField(default=1)
    def __str__(self):
        return f'{self.default_weapon.name}.LV{self.level}'

class Character(models.Model):
    nickname = models.CharField(max_length=20)
    weapon = models.OneToOneField(Weapon, on_delete=models.SET_NULL, related_name='character_who_have', null=True, blank=True)
    coin = models.BigIntegerField(default = 0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='character', null=True, blank=True)
    inventory = models.ManyToManyField(LuckyItem, related_name='characters_who_have', blank=True)
    def __str__(self):
        return f'{self.nickname} - {self.user.username}'

class Enemy(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    hp = models.IntegerField()
    def __str__(self):
        return f'{self.name}.LV{self.level}'

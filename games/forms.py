from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    nickname = forms.CharField(label="닉네임을 입력해주세요", max_length=20)
    class Meta:
        model = Character
        fields = ['nickname',]

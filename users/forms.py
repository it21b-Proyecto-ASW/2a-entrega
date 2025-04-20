from django import forms
from .models import UserProfile

class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class ProfileBioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']

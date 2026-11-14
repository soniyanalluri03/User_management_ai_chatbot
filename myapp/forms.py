from django import forms
from .models import profile

class ProfileForm(forms.ModelForm):
    class Meta:                                                     #usees how the form behves
        model = profile
        fields = ['gender', 'age', 'height', 'weight']                   #profile table
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile,Exercises

class CreateUser(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']

class UserUpdate(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdate(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['image']
        
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercises
        fields = ['name', 'type', 'intensity']
        widgets = {
            'intensity': forms.Select(choices=Exercises.INTENSITY,attrs={'class': 'intensity-field'})
        }
# class Create(forms.Form):
#     name = forms.CharField(max_length=100, label='Name')
#     type = forms.CharField(label='type', max_length=50)

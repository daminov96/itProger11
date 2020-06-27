from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile


class UserOurRegistration(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileImage(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileImage, self).__init__(*args, **kwargs)
        self.fields['img'].label = 'Image profile'

    class Meta:
        model = Profile
        fields = ['img']
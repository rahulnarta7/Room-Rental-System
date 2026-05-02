from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        from django.contrib.auth.models import User

        # Check if email exists
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                raise forms.ValidationError("User not found")
        else:
            username = username_or_email

        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Invalid credentials")

        self.user = user
        return data
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
             'title',
            'price',
            'location',
            'full_address',
             'description',
             'room_type',
            'contact_phone',
            'contact_email',
            'image1',
            'image2',
            'image3',
            'image4'
]
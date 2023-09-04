from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = User
        fields = {'email', 'username', 'password1', 'password2'}
    field_order = ['email', 'username',]
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = User.objects.exclude(pk=self.instance.pk).get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError("Email {} is already in use.".format(email))
    

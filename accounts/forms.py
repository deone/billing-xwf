import hashlib

from django import forms

from .models import Radcheck

class CreateAccountForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=100, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    password = forms.CharField(label='Password', max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, 
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")

    def save(self):
        data = self.cleaned_data
        m = hashlib.md5()
        byte_encode = bytes(data['password'], 'utf-8')
        m.update(byte_encode)
        Radcheck.objects.create(username=data['email'],
                                attribute='MD5-Password',
                                op=':=',
                                value=m.hexdigest())
        return True

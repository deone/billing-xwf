from django import forms

class createAccountForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, widget=forms.PasswordInput)

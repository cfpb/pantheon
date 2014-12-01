from django import forms
from django.utils.safestring import mark_safe

class NameForm(forms.Form):
    update_public_name = forms.BooleanField(required=False)
    updated_name = forms.CharField(max_length=100, required=False)

    def clean(self):
        data = self.cleaned_data
        if data.get('update_public_name') and not data.get('updated_name'):
            raise forms.ValidationError("'Updated Name' is required if you want to update your public name.")

class PublicizeForm(forms.Form):
    make_membership_public = forms.BooleanField(required=False, help_text='Become a proud public member of our org.')

class PubKeyForm(forms.Form):
    add_public_key = forms.BooleanField(required=False, help_text='Do you want to add the following GitHub Enterprise key to your public GitHub account?')
    key_to_add = forms.ChoiceField(choices=[], required=False)
    key_name = forms.CharField(max_length=20, required=False)

    def clean(self):
        data = self.cleaned_data
        if data.get('add_public_key') and (not data.get('key_to_add') or not data.get('key_name')):
            raise forms.ValidationError("'Key To Add' and 'Key Name' are required if you want to add a public key.")

class TwoFactorAuthForm(forms.Form):
    two_factor = forms.BooleanField(label='I certify I have enabled two factor authentication', help_text=mark_safe('You MUST <a href="https://help.github.com/articles/about-two-factor-authentication/">enable two factor authentication</a> before requesting membership.'))

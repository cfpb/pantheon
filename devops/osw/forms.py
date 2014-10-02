from django import forms

class NameForm(forms.Form):
    update_public_name = forms.BooleanField(required=False)
    updated_name = forms.CharField(max_length=100, required=False)

class PublicizeForm(forms.Form):
    make_membership_public = forms.BooleanField(required=False, help_text="Become a proud public member of our org.")

from django import forms

class EnterpriseDetailsForm(forms.Form):
    fullname = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    location = forms.CharField(max_length=100)
    contractor = forms.BooleanField(required=False)
from django import forms

class EnterpriseDetailsForm(forms.Form):
    fullname = forms.CharField(max_length=100)
    email = forms.EmailField()
    location = forms.CharField(max_length=100, help_text='City/State if remote; Floor or Desk number if DC.')
    contractor = forms.BooleanField(required=False)

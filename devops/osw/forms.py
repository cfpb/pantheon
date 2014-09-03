from django import forms


class StartForm(forms.Form):
    repo_name = forms.CharField()

class ReleaseForm(forms.Form):
    repo = forms.ChoiceField(choices=tuple())

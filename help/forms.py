from django import forms

class HelpSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

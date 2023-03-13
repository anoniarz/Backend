from django import forms


class Url_f(forms.Form):
    url_f = forms.CharField(label="Enter your string", max_length=55)

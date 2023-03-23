from django import forms


class Url_f(forms.Form):
    url_f = forms.CharField(label="Enter ceneo id/url", max_length=55)


class ReviewFilterForm(forms.Form):
    STARS_CHOICES = [(i/2, f"{i/2}") for i in range(0, 11)]
    stars = forms.MultipleChoiceField(
        choices=STARS_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    recommendation = forms.MultipleChoiceField(
        choices=[('True', 'Yes'), ('False', 'No'), ('None', 'None')], required=False, widget=forms.CheckboxSelectMultiple)
    is_verified = forms.BooleanField(required=False)
    days_used = forms.IntegerField(required=False)
    t_up = forms.IntegerField(required=False)
    t_down = forms.IntegerField(required=False)
    pos_features = forms.IntegerField(required=False)
    neg_features = forms.IntegerField(required=False)

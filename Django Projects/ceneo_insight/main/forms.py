from django import forms


class Url_f(forms.Form):
    url_f = forms.CharField(label="Enter your string", max_length=55)
    
    
class ReviewFilterForm(forms.Form):
    stars = forms.IntegerField(required=False)
    recommendation = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], required=False)
    is_verified = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')], required=False)
    days_used = forms.IntegerField(required=False)
    t_up = forms.IntegerField(required=False)
    t_down = forms.IntegerField(required=False)
    pos_features = forms.CharField(max_length=100, required=False)
    neg_features = forms.CharField(max_length=100, required=False)
from django import forms
from geelweb.django.ratings.widgets import StarRadioFieldRenderer

class RatingForm(forms.Form):
    RATING_CHOICES = ((1,1), (2,2), (3,3), (4,4))

    rating = forms.CharField(
            label='',
            widget=forms.RadioSelect(renderer=StarRadioFieldRenderer, attrs={'class':'star required'}, choices=RATING_CHOICES))
    comment = forms.CharField(label='Add a comment ?', widget=forms.Textarea)


from django import forms
from .models import Category


categories = Category.objects.all()
options = [("", "Select Category (Optional)"),]
   
for category in categories:
    options.append((category.id, category))

options = tuple(options)

class CreateListingForm(forms.Form):
    
    title = forms.CharField(
        max_length=150,   
    )
    
    description = forms.CharField( 
        max_length=1024, 
        required=False,
        widget=forms.Textarea(
            attrs={"rows":3}
        )
    )

    img_url = forms.URLField(
        required=False, 
    )

    starting_bid = forms.FloatField(
        min_value=1, 
    )

    category = forms.ChoiceField(
        choices=options, 
        required=False,
    )
    
    
    title.widget.attrs.update({'class': 'mt-4 form-control', 'placeholder':'Title', 'autocomplete': 'off'})
    description.widget.attrs.update({'class': 'mt-2 form-control', 'placeholder':'Description (Optional)'})
    img_url.widget.attrs.update({'class': 'mt-2 form-control', 'placeholder':'Image URL (Optional)', 'autocomplete': 'off'})
    starting_bid.widget.attrs.update({'class': 'mt-2 form-control', 'placeholder':'Starting Bid (USD)'})
    category.widget.attrs.update({'class': 'mt-2 form-control'})


class BiddingForm(forms.Form):

    bid = forms.FloatField()

    bid.widget.attrs.update({'class': 'form-control form-control-sm mr-2 w-25', 'placeholder':'Bid (USD)'})


class CommentForm(forms.Form):
    
    comment = forms.CharField(
        max_length=1024,   
    )
    
    comment.widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'Your comment goes here...', 'autocomplete': 'off'})
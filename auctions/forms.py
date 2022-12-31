from email.policy import default

from .models import Listing
from django.forms import ModelForm

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = [
            'date_made',
            'user',
            'category',
            'is_active',
            'watchlist'
        ]





'''class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'  '''

from django.forms import ModelForm
from .models import stock_item,stock_total

class stockTotalForm(ModelForm):
    class Meta:
        model = stock_total
        fields=['importer', 'items']

#class stockItemForm(ModelForm):
 #   class Meta:
 #       model=stock_item
  #      fields = ['items', 'quantity']


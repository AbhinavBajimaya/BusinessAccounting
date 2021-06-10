from django.forms import ModelForm
from .models import stock_item,stock_total,Item



class stockTotalForm(ModelForm):
    class Meta:
        model = stock_total
        fields=['importer', 'items']


class stockItemForm(ModelForm):
    class Meta:
        model=stock_item
        fields = [ 'items' ,'quantity']

class createItemForm(ModelForm):
    class Meta:
        model= Item
        fields = ['item_type', 'model_name', 'company_name',
                   'price', 'description']




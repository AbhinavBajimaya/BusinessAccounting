from django.forms import ModelForm
from .models import stock_item,stock_total,Item,Importer



class stockTotalForm(ModelForm):
    class Meta:
        model = stock_total
        fields=['importer', 'items','total_price']

    def __init__(self, *args, **kwargs):
        super(stockTotalForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = stock_item.objects.filter(current=True)


class stockItemForm(ModelForm):
    class Meta:
        model=stock_item
        fields = [ 'items' ,'quantity','in_price','current','total_price']
        

class createItemForm(ModelForm):
    class Meta:
        model= Item
        fields = ['item_type', 'model_name', 'company_name',
                   'price', 'description']

class createImporterForm(ModelForm):
    class Meta:
        model = Importer
        fields = ['name','owner_name','address','phone_number','vat_number','pan_number']






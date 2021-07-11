from django.forms import ModelForm
from .models import stock_item,stock_total,Item,Importer,Customer,sale_item,sale_total



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


#############################################################################################

class saleTotalForm(ModelForm):
    class Meta:
        model = sale_total
        fields = ['customer', 'items', 'total_price']

    def __init__(self, *args, **kwargs):
        super(saleTotalForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = sale_item.objects.filter(current=True)


class saleItemForm(ModelForm):
    class Meta:
        model = sale_item
        fields = ['items', 'quantity', 'sale_price', 'current', 'total_price']


class createCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'owner_name', 'address', 'phone_number', 'vat_number', 'pan_number']






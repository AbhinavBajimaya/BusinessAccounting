from django.forms import ModelForm
from .models import stock_item,stock_total,Item,Importer,Customer,sale_item,sale_total,Item_type




class stockTotalForm(ModelForm):
    
    class Meta:
        model = stock_total
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(stockTotalForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = stock_item.objects.filter(current=True)


class stockItemForm(ModelForm):
    class Meta:
        model=stock_item
        fields = '__all__'
        

class createItemForm(ModelForm):
    class Meta:
        model= Item
        fields = '__all__'

class createImporterForm(ModelForm):
    class Meta:
        model = Importer
        fields = '__all__'


#############################################################################################

class saleTotalForm(ModelForm):
    class Meta:
        model = sale_total
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(saleTotalForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = sale_item.objects.filter(current=True)


class saleItemForm(ModelForm):
    class Meta:
        model = sale_item
        fields = '__all__'


class createCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'






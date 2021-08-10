from django.db import models
from pyBSDate import convert_AD_to_BS,bsdate
import datetime



# Create your models here

#name and description of individual items.
class Item_type(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Item(models.Model):
    item_type = models.ForeignKey(Item_type, on_delete=models.PROTECT)
    model_name = models.CharField(max_length=50,null=True,default='none')
    company_name=models.CharField(max_length=50,null=True,default='none')
    size=models.CharField(max_length=30,null=True,blank=True)
    quantity=models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)  
    is_stock=models.BooleanField(default=True)
    total_in_quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        if str(self.size)=="None":
            return self.item_type.name + " " + self.model_name + " " + self.company_name
        else:
            return self.item_type.name + " " + self.model_name + " " + self.size + " " + self.company_name

    def set_is_stock(self):
        if self.quantity == 0:
            self.is_stock=False
        else:
            self.is_stock=True
        self.save()
        

#from where items are imported
class Importer(models.Model):
    name=models.CharField(max_length=50)
    owner_name=models.CharField(max_length=50,blank=True,null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vat_number = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    pan_number = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    total_credit = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    def __str__(self):
        return self.name 

#details of customer
class Customer(models.Model):
    name = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vat_number = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True)
    pan_number = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    total_credit = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    def __str__(self):
        return self.name

#individual items and quantities on stocking
class stock_item(models.Model):    
    current=models.BooleanField(default=True)
    items=models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    in_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return "(" + str(self.quantity) + ")" + self.items.model_name + " at "  + str(self.in_price) + " = " + str(self.in_price*self.quantity)
  
#total bill transactions and list of items/quantities on stocking
class stock_total(models.Model):
    importer=models.ForeignKey(Importer, on_delete=models.PROTECT)
    items=models.ManyToManyField(stock_item)
    added_at = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2,default=0)
    total_paid = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    
    def __str__(self):
        a=self.added_at
        b=convert_AD_to_BS(a.year, a.month, a.day)
        c = bsdate(b[0], b[1], b[2]).strftime("%B %d %Y, %A", lang='en')
        return self.importer.name + " " + str(c)
    def get_total_price(self):
        total = 0
        for item in items:
            total += item.total_price
        return total
    
    
#individual items and quantities on sales
class sale_item(models.Model):
    current = models.BooleanField(default=True)
    items = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return "(" + str(self.quantity) + ")" + self.items.model_name + " at " + str(self.sale_price) + " = " + str(self.sale_price*self.quantity)

#total sale bill items and quantities    
class sale_total(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    items=models.ManyToManyField(sale_item)  
    sold_att = models.DateField(auto_now_add=True)  
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    def __str__(self):
        a = self.sold_att
        b = convert_AD_to_BS(a.year, a.month, a.day)
        c = bsdate(b[0], b[1], b[2]).strftime("%B %d %Y, %A", lang='en')
        return self.customer.name + " " + str(c)
    def get_total_price(self):
        total = 0
        for item in items:
            total += item.total_price
        return total

class account(models.Model):
    name=models.CharField(max_length=40)
    expense_out = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    revenue_in  = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    stock_price  = models.DecimalField(max_digits=12, decimal_places=2,default=0)    
    def get_stock_price(self):
        sum=0
        for item in Item.objects.filter(is_stock=True):
            total=item.quantity*item.price
            sum += total
        self.stock_price=sum
        self.save()
        return self.stock_price
    def __str__(self):
        return self.name

    
#in the case of customer returning an item
#class return_item(models.Model):
 #   customer=models.ForeignKey(Customer, on_delete=models.PROTECT)
  #  items=models.ForeignKey(Item, on_delete=models.PROTECT)
   # quantity=models.PositiveIntegerField()
    #returned_at=models.DateTimeField(auto_now_add=True)


    






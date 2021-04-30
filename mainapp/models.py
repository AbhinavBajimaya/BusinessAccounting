from django.db import models
import datetime


# Create your models here

#name and description of individual items.
class Item(models.Model):
    name=models.CharField(max_length=50)
    company_name=models.CharField(max_length=50)
    item_type=models.CharField(max_length=30)
    quantity=models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description=models.TextField(max_length=100)

    def __str__(self):
        return self.name

#from where items are imported
class Importer(models.Model):
    name=models.CharField(max_length=50)
    owner_name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    phone_number=models.DecimalField(max_digits=10, decimal_places=0)
    vat_number=models.DecimalField(max_digits=15, decimal_places=0)
    pan_number=models.DecimalField(max_digits=15, decimal_places=0)

    def __str__(self):
        return self.name 

#details of customer
class Customer(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    phone_number=models.DecimalField(max_digits=10, decimal_places=0)
    vat_number=models.DecimalField(max_digits=15, decimal_places=0)
    pan_number=models.DecimalField(max_digits=15, decimal_places=0)

    def __str__(self):
        return self.name

#individual items and quantities on stocking
class stock_item(models.Model):
    importer=models.ForeignKey(Importer, on_delete=models.PROTECT)
    items=models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.importer.name + " " + self.items.name + " " + str(self.quantity)

#total bill transactions and list of items/quantities on stocking
class stock_total(models.Model):
    items=models.ManyToManyField(stock_item)

    def __str__(self):
        importer_name=self.items.first()
        return importer_name.importer.name + " " + importer_name.added_at.strftime('%m/%d/%Y')

#individual items and quantities on sales
class sale_item(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    items=models.ForeignKey(Item,on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name + " "  + self.items.name + " " + self.quantity


#total sale bill items and quantities    
class sale_total(models.Model):
    items=models.ManyToManyField(sale_item)    

    def __str__(self):
        customer_name=self.items.first()
        return customer_name.customer.name + " " + customer_name.sold_at.strftime('%m%d%y')

#in the case of customer returning an item
class return_item(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT)
    items=models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    returned_at=models.DateTimeField(auto_now_add=True)






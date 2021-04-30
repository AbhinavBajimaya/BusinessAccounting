from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Item)
admin.site.register(Importer)
admin.site.register(Customer)
admin.site.register(stock_item)
admin.site.register(stock_total)
admin.site.register(sale_item)
admin.site.register(sale_total)
#admin.site.register()
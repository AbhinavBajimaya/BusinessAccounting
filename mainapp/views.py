from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .import models
from .forms import stockTotalForm,stockItemForm,createItemForm,createImporterForm,saleItemForm,saleTotalForm,createCustomerForm
from datetime import datetime
import time

# Create your views here.



def home_view(request):
    return render(request, 'mainapp/home.html')

def view_all_stock_view(request):
    allstock=models.Item.objects.filter(is_stock=True)
    obj=models.account.objects.first()
    stock_price=obj.get_stock_price()
    
    context={
        "allstock": allstock,
        "stock_price": stock_price

    }
    return render(request, 'mainapp/allstock.html' ,context)

def buy_item_view(request):
    if request.method == 'POST':
        form1=stockTotalForm(request.POST) 
        if form1.is_valid():   
            for item in (models.stock_item.objects.filter(current=True)):
                item.current=False
                item.items.total_in_quantity += item.quantity
                item.items.quantity += item.quantity
                item.items.save()
                item.save()
                item.items.set_is_stock()            
            form1.save()

            last_in = models.stock_total.objects.last()
            account=models.account.objects.first()
            last_importer=last_in.importer
            last_importer.total_amount += last_in.total_price
            last_importer.total_credit +=last_in.credit
            account.expense_out += last_in.total_price
            last_importer.save()
            account.save()
                        
            return redirect('home')
    else:
        
        form1= stockTotalForm()
    return render(request, 'mainapp/buyitem.html', {'form1':form1 })


def add_item_view(request):
    if request.method=='POST':
        form2=stockItemForm(request.POST)
        if form2.is_valid():
            in_price_cost =request.POST.get('in_price')
            print(in_price_cost)
            item=form2.cleaned_data['items']
            form2.save()
            if in_price_cost==item.price:
                pass
            else:
                item_select=models.Item.objects.get(id=item.id)
                item_select.price=in_price_cost
                item_select.save()
                
            return redirect('buyitems')
    else:
        form2=stockItemForm()
    return render(request, 'mainapp/additem.html', {'form2':form2 })

def create_new_item_view(request, way):
    if request.method == 'POST':
        form3 = createItemForm(request.POST)
        if form3.is_valid():
            form3.save()
            if way==1:
                return redirect('additem')
            else:
                return redirect('home')
    else:
        form3=createItemForm()
    
    return render(request, 'mainapp/createnewitem.html', {'form3':form3 })
    
def view_all_importers(request):
    importers=models.Importer.objects.all()
    return render(request, 'mainapp/viewimporters.html', {'importers' :importers})

def imp_detail(request ,id):
    importer = models.Importer.objects.get(id=id)
    return render(request, 'mainapp/impdetail.html', {'importer': importer})




def create_importer(request):
    if request.method=='POST':
        form=createImporterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=createImporterForm()
    return render(request, 'mainapp/createimporter.html', {'form' :form})

#new

def view_all_customers(request):
    customers = models.Customer.objects.all()
    return render(request, 'mainapp/viewcustomers.html', {'customers': customers})


def create_customer(request):
    if request.method == 'POST':
        form = createCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = createCustomerForm()
    return render(request, 'mainapp/createcustomer.html', {'form': form})

def cus_detail(request ,id):
    customer = models.Customer.objects.get(id=id)
    return render(request, 'mainapp/cusdetail.html', {'customer': customer})



def sale_item_view(request):
    if request.method == 'POST':
        form1 = saleTotalForm(request.POST)
        if form1.is_valid():
            for item in (models.sale_item.objects.filter(current=True)):
                item.current = False
                item.items.quantity -= item.quantity
                item.items.save()
                item.save()
                item.items.set_is_stock()
            form1.save()
            last_in = models.sale_total.objects.last()
            last_customer = last_in.customer
            last_customer.total_amount += last_in.total_price
            last_customer.total_credit += last_in.credit
            account = models.account.objects.first()
            account.revenue_in += last_in.total_price
            last_customer.save()
            account.save()
            return redirect('home')
    else:
        form1 = saleTotalForm()
        a = models.sale_item.objects.filter(current=True)
        sum = 0
        for b in a:
            sum += b.items.price*b.quantity

    return render(request, 'mainapp/saleitem.html', {'form1': form1, 'sum': sum})


def add_sale_item_view(request):
    if request.method == 'POST':
        form2 = saleItemForm(request.POST)
        if form2.is_valid():
            quantity = request.POST.get('quantity')
            item =request.POST.get('items')
            print(item)
            req_item=models.Item.objects.get(id=item)
            if int(quantity) < req_item.quantity:
                form2.save()
                a=models.sale_item.objects.filter(current=True)
                sum=0
                for b in a :
                    sum += b.items.price*b.quantity

                form1=saleTotalForm()
                return render(request, 'mainapp/saleitem.html', {'form1': form1, 'sum': sum})
                #return redirect('saleitems')
            else:
                return HttpResponseRedirect('Error')
    else:
        form2 = saleItemForm()
    return render(request, 'mainapp/addsaleitem.html', {'form2': form2})


def view_credit_importers(request):
    importers = models.Importer.objects.exclude(total_credit=0)
    return render(request, 'mainapp/viewcreditimporters.html', {'importers': importers})
        
def imp_credit_detail(request, id):
    importer = models.Importer.objects.get(id=id)

    if request.method == 'POST':
        credit=request.POST['credit']
        importer.total_credit -= int(credit)
        
        importer.save()
        #enter success message here#
        
        return redirect('viewcreditimporters')
        

    return render(request, 'mainapp/impcreditdetail.html', {"importer": importer})


def view_credit_customers(request):
    customers = models.Customer.objects.exclude(total_credit=0)
    return render(request, 'mainapp/viewcreditcustomers.html', {'customers': customers})
        
def cus_credit_detail(request, id):
    customer = models.Customer.objects.get(id=id)

    if request.method == 'POST':
        credit=request.POST['credit']
        customer.total_credit -= int(credit)
        
        customer.save()
        #enter success message here#
        
        return redirect('viewcreditcustomers')
        

    return render(request, 'mainapp/cuscreditdetail.html', {"customer": customer})
        
    






    
    
    






    

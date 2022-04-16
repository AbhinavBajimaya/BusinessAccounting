from typing import ContextManager
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .import models
from .forms import stockTotalForm,stockItemForm,createItemForm,createImporterForm,saleItemForm,saleTotalForm,createCustomerForm,ItemCategoryForm
from datetime import datetime
import time
import pyBSDate
import json
import numpy as np
import pandas as pd




# Create your views here.



def home_view(request):
    account = models.account.objects.last()
    sales=models.sale_total.objects.all()
    profit=0
    for i in sales:
        profit += i.profit

    #current month
    daysales=[]
    dayprofit=[]
    #get current nepali date month year
    #access all sale records of current date month
    datetoday=datetime.now()
    y=int(datetoday.strftime("%Y"))
    m=int(datetoday.strftime("%m"))
    d=int(datetoday.strftime("%d"))

    nepalidate=pyBSDate.convert_AD_to_BS(y,m,d)
    #print(nepalidate)

    for i in range(1,34):
        try:
            b=pyBSDate.convert_BS_to_AD(nepalidate[0],nepalidate[1],i)
        except:
            break;
    i -=1
    #change to current
    start=pyBSDate.convert_BS_to_AD(nepalidate[0],nepalidate[1],1)
    end=pyBSDate.convert_BS_to_AD(nepalidate[0],nepalidate[1],30)

    start_date=str(start[0])+'-'+str(start[1])+'-'+str(start[2])
    end_date=str(end[0])+'-'+str(end[1])+'-'+str(end[2])

    sale_list=models.sale_total.objects.filter(sold_att__range=[start_date,end_date])
    
    dict={}
    for date in range(i):
        #if len(str(date))==1:
        #  date='0'+str(date)
        dict[str(nepalidate[0])+'-'+str(nepalidate[1])+'-'+ str(date)]={'sales':0, 'profit':0}
    
    for sale in sale_list:
        y=int(sale.sold_att.strftime("%Y"))
        m=int(sale.sold_att.strftime("%m"))
        d=int(sale.sold_att.strftime("%d"))
        date2=pyBSDate.convert_AD_to_BS(y,m,d)
        dict[str(date2[0])+'-'+str(date2[1])+'-'+str(date2[2])]['sales']+=sale.total_price
        dict[str(date2[0])+'-'+str(date2[1])+'-'+str(date2[2])]['profit']+=sale.profit

    daylist=[]
    saleslist=[]
    profitlist=[]
    for i in dict.keys():
        daylist.append(i)
        saleslist.append(int(dict[i]['sales']))
        profitlist.append(int(dict[i]['profit']))
    #current year
    context={
        "account":account,
        "profit":profit,
        "daylist":daylist,
        "saleslist":saleslist,
        "profitlist":profitlist
    }
    return render(request, 'mainapp/home.html',context)

def view_all_stock_view(request):
    if request.method == 'POST':
        name= request.POST.get('itemtypes')
        itemtypes=models.Item_type.objects.all()
        itemtype=models.Item_type.objects.get(name=name)
        allstock=models.Item.objects.filter(item_type = itemtype).filter(is_stock=True)
        context={
            'itemtypes' : itemtypes,
            "allstock": allstock,
            'itemtype': itemtype
        }
        
    else:
        itemtypes=models.Item_type.objects.all()
        allstock=models.Item.objects.filter(is_stock=True)
        obj=models.account.objects.first()
        stock_price=obj.get_stock_price()   
        context={
            'itemtypes' : itemtypes,
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
    imp=models.Importer.objects.all().values()
    df=pd.DataFrame(imp)
    df1=df.name.tolist()
    df=df['total_amount'].tolist()
    df2=[]
    for i in df:
        df2.append(int(i))
    return render(request, 'mainapp/viewimporters.html', {'importers' :importers,'df1':df1,'df2':df2})

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
            req_item=models.Item.objects.get(id=item)
            if int(quantity) <= req_item.quantity:
                form2.save()   
                return redirect('saleitems')
            else:
                return HttpResponseRedirect('itemnotinstock')
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
    total=0
    for customer in customers:
        total += customer.total_credit 
        
    return render(request, 'mainapp/viewcreditcustomers.html', {'customers': customers, 'total': total})
        
def cus_credit_detail(request, id):
    customer = models.Customer.objects.get(id=id)

    if request.method == 'POST':
        credit=request.POST['credit']
        customer.total_credit -= int(credit)
        
        customer.save()
        #enter success message here#
        
        return redirect('viewcreditcustomers')
        

    return render(request, 'mainapp/cuscreditdetail.html', {"customer": customer})

def view_month_report(request):
    month=request.POST.get('month')
    year=request.POST.get('year')
    for i in range(1,34):
        try:
            b=pyBSDate.convert_BS_to_AD(year,month,i)
        except:
            break;
    i -=1

    start=pyBSDate.convert_BS_to_AD(year,month,1)
    end=pyBSDate.convert_BS_to_AD(year,month,i)

    start_date=str(start[0])+'-'+str(start[1])+'-'+str(start[2])
    end_date=str(end[0])+'-'+str(end[1])+'-'+str(end[2])
    sale_list=models.sale_total.objects.filter(sold_att__range=[start_date,end_date])
    income=0
    profit = 0
    for sale in sale_list:
        income += sale.total_price
        profit += sale.profit
        
    
    context={
        "sale_list":sale_list,
        "profit": profit,
        "income": income
    }

    return render(request, 'mainapp/monthreport.html',context)

def view_sale_report(request, id):
    sale_report = models.sale_total.objects.get(id=id)
    return render(request, 'mainapp/sale_report.html', {"sale_report": sale_report})

def getreportbytype(request):
    sale_list={}
    item_types=models.Item_type.objects.all()
    for item in item_types:
        sale_list[item.name]=0
    allsaleitems=models.sale_item.objects.all()
    for i in allsaleitems:
        sale_list[i.items.item_type.name] += int(i.total_price)
    return render(request, 'mainapp/reportbytype.html', {"sale_list": sale_list})

       
    






            

        
    






    
    
    






    

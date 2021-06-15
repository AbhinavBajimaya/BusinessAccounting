from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .import models
from .forms import stockTotalForm,stockItemForm,createItemForm
from datetime import datetime

# Create your views here.



def home_view(request):
    return render(request, 'mainapp/home.html')

def view_all_stock_view(request):
    allstock=models.Item.objects.filter(is_stock=True)
    context={
        "allstock": allstock,

    }
    return render(request, 'mainapp/allstock.html' ,context)

def buy_item_view(request):
    if request.method == 'POST':
        form1=stockTotalForm(request.POST) 
        if form1.is_valid():
            items=request.POST.get('items')
            print(items)
            #for item in (models.stock_item.objects.filter(current=True)):
            #    item.current=False
            #    item.items.quantity += item.quantity
            #    item.items.save()
            #    item.save()
            #    item.items.set_is_stock()
                
            #form1.save()
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
    
    
    
    






    

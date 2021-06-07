from django.shortcuts import render
from django.http import HttpResponseRedirect
from .import models
from .forms import stockTotalForm,stockItemForm


# Create your views here.
def home_view(request):
    return render(request, 'mainapp/home.html')

def view_all_stock_view(request):
    allstock=models.Item.objects.filter(in_stock=True)
    context={
        "allstock": allstock,

    }
    return render(request, 'mainapp/allstock.html' ,context)

#def buy_item_view(request):
 #   if request.method == 'POST':
  #      form=stockTotalForm(request.POST)
   #     if form.is_valid():
    #        #form.save()
     #       return HttpResponseRedirect('success')
    #else:
     #   form1= stockTotalForm()
     #   form2=stockItemForm()
    #return render(request, 'mainapp/buyitem.html', {'form1':form1 , 'form2':form2})


    

from django.urls import path
from . import views

urlpatterns=[
    path('',views.home_view,name="home"),
    path('viewstock', views.view_all_stock_view, name="viewstock"),
    #path('buyitems', views.buy_item_view, name="buyitem"),
]
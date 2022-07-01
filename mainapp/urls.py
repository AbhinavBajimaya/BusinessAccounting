from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns=[
    path('',views.home_view,name="home"),       
    path('viewstock', views.view_all_stock_view, name="viewstock"),
    
    #buying portion
    path('buyitems', views.buy_item_view, name="buyitems"),
    path('additem', views.add_item_view, name="additem"),
    path('createitem/<int:way>/', views.create_new_item_view, name='createitem'),
    path('createimporter',views.create_importer, name='createimporter'),
    path('viewimporters',views.view_all_importers,name='viewimporters'),

    #selling portion
    path('saleitems', views.sale_item_view, name="saleitems"),
    path('addsaleitem', views.add_sale_item_view, name="addsaleitem"),
    path('createcustomer', views.create_customer, name='createcustomer'),
    path('viewcustomers', views.view_all_customers, name='viewcustomers'),

    #credits portion
    path('viewcreditimporters',views.view_credit_importers, name='viewcreditimporters'),
    path('impcreditdetail/<int:id>/',views.imp_credit_detail,name='impcreditdetail'),
    
    path('viewcreditcustomers',views.view_credit_customers, name='viewcreditcustomers'),
    path('cuscreditdetail/<int:id>/',views.cus_credit_detail,name='cuscreditdetail'),

    path('impdetail/<int:id>/',views.imp_detail, name='impdetail'),
    path('cusdetail/<int:id>/',views.cus_detail, name='cusdetail'),

    path('monthreport',views.view_month_report,name='monthreport'),
    path('monthreport/salereport/<int:id>/',views.view_sale_report, name='salereport'),

    path('reportbytype',views.getreportbytype,name='getreportbytype'),
    path('export',views.export_to_csv,name='export'),


]

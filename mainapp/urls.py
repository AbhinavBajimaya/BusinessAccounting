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
    path('viewimporters',views.view_all_importers,name='viewimporters')
]

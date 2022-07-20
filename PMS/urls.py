"""PMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index

urlpatterns = [
	path('admin/', admin.site.urls),
	path('addproduct/', index.AddProduct),
	path('deleteproduct/', index.DeleteProduct),
	path('addinventory/', index.AddInventory),
	path('updateproduct/', index.UpdateProduct),
	path('idsearchproductupdate/', index.SearchProductByIDForUpdate),
	path('namesearchproductupdate/', index.SearchProductByNameForUpdate),
	path('idsearchproductinventory/', index.SearchProductByIDForInv),
	path('namesearchproductinventory/', index.SearchProductByNameForInv),
	path('idsearchproductbill/', index.SearchProductByIDForBill),
	path('namesearchproductbill/', index.SearchProductByNameForBill),
	path('displayinventoryforbill/', index.DisplayInvForBill),
	path('addtocart/', index.AddInvToCart),
	path('removefromcart/', index.RemoveFromCart),
	path('totalbill/', index.TotalBill),
	path('savebill/', index.SaveBill),
	path('loadstockalert/', index.LoadStockAlert),
	path('loadexpalert/', index.LoadExpAlert),
	path('displayinventory/', index.DisplayInv),
	path('deleteinventory/', index.DeleteInventory),
	path('displayreport/', index.Report),
	path('', index.index, name='index'),
]

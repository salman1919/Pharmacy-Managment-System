from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from datetime import date
import pyodbc


def index(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	cursor = conn.cursor()
	cursor.execute("truncate table bill")
	return render(request, 'index.html')


def LoadStockAlert(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		cursor = conn.cursor()
		cursor.execute(
			"select a.ProductId, a.ProductName, a.MinStockLimit, a.Total from (select Inventory.ProductId,Product.ProductName,Product.MinStockLimit,Sum(Inventory.Quantity) as Total from Product inner join Inventory on Inventory.ProductId=Product.ProductId group by Inventory.ProductId , Product.ProductName,Product.MinStockLimit )a where a.MinStockLimit > a.Total")
		result = cursor.fetchall()
		return render(request, 'stockalert.html', {'StockAlert': result})


def LoadExpAlert(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		currentdate = date.today()
		cursor = conn.cursor()
		cursor.execute(
			"select * from Product inner join Inventory on Product.ProductId=Inventory.ProductId where (Inventory.ExpiryDate)<'%s'" % currentdate)
		result = cursor.fetchall()
		return render(request, 'expalert.html', {'ExpAlert': result})


def AddProduct(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		values = Product()
		values.ProId = request.POST.get('ProId')
		values.ProName = request.POST.get('ProName')
		values.MinLimit = request.POST.get('MinLimit')
		values.ComName = request.POST.get('ComName')
		values.UCost = request.POST.get('UCost')
		values.RCost = request.POST.get('RCost')
		values.ShelfNo = request.POST.get('ShelfNo')
		cursor = conn.cursor()
		cursor.execute(
			"Insert into Product values ('" + values.ProId + "','" + values.ProName + "','" + values.MinLimit + "','" + values.ComName + "','" + values.UCost + "','" + values.RCost + "','" + values.ShelfNo + "')")
		cursor.commit()
		return HttpResponse('')


def DeleteProduct(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		ProId = request.POST.get('ProId')
		cursor = conn.cursor()
		cursor.execute("delete from Product where ProductId='%s'" % ProId)
		cursor.commit()
		return HttpResponse("")


def SearchProductByIDForUpdate(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pid = request.POST.get('SearchID')
		pid = pid + "%"
		cursor = conn.cursor()
		cursor.execute("select * from Product where ProductId like '%s' order by ProductName ASC " % pid)
		result = cursor.fetchall()

		return render(request, 'product.html', {'getdata': result})


def SearchProductByNameForUpdate(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pn = request.POST.get('SearchName')
		pn = pn + "%"
		cursor = conn.cursor()
		cursor.execute("select * from Product where ProductName like '%s' order by ProductName ASC " % pn)
		result = cursor.fetchall()

		return render(request, 'product.html', {'getdata': result})


def UpdateProduct(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		ProId = request.POST.get('ProId')
		ProName = request.POST.get('ProName')
		MinLimit = request.POST.get('MinLimit')
		ComName = request.POST.get('ComName')
		UCost = request.POST.get('UCost')
		RCost = request.POST.get('RCost')
		ShelfNo = request.POST.get('ShelfNo')
		cursor = conn.cursor()
		cursor.execute(
			"update Product set ProductId='%s', ProductName='%s' , MinStockLimit ='%s' , CompanyName='%s' , CostPerUnit='%s' , SalePerUnit='%s' , ShelfNo='%s' where ProductId='%s'" % (
				ProId, ProName, MinLimit, ComName, UCost, RCost, ShelfNo, ProId))
		cursor.commit()
		return HttpResponse('')


def SearchProductByIDForInv(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pid = request.POST.get('SearchID')
		pid = pid + "%"
		cursor = conn.cursor()
		cursor.execute("select * from Product where ProductId like '%s' order by ProductName ASC" % pid)
		result = cursor.fetchall()

		return render(request, 'inventory.html', {'getdata': result})


def SearchProductByNameForInv(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pn = request.POST.get('SearchName')
		pn = pn + "%"
		cursor = conn.cursor()
		cursor.execute("select * from Product where ProductName like '%s' order by ProductName ASC" % pn)
		result = cursor.fetchall()

		return render(request, 'inventory.html', {'getdata': result})


def AddInventory(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		PId = request.POST.get('ProIdInv')
		InvId = request.POST.get('InvId')
		BatchNo = request.POST.get('BatchNo')
		Quantity = request.POST.get('InvQuantity')
		InvExp = request.POST.get('InvExp')
		cursor = conn.cursor()
		cursor.execute(
			"Insert into Inventory values ('%s','%s','%s','%s','%s')" % (PId, InvId, BatchNo, Quantity, InvExp))
		cursor.commit()
		return HttpResponse('')


def DisplayInv(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pid = request.POST.get('SearchId')
		pid = pid + "%"
		cursor = conn.cursor()
		cursor.execute("select * from inventory where ProductId like '%s' order by ExpiryDate ASC " % pid)
		result = cursor.fetchall()

		return render(request, 'invlist.html', {'getInv': result})


def DeleteInventory(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		InvId = request.POST.get('InvId')
		cursor = conn.cursor()
		cursor.execute("delete from Inventory where InventoryId='%s'" % InvId)
		cursor.commit()
		return HttpResponse("")


def SearchProductByIDForBill(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pid = request.POST.get('SearchID')
		pid = pid + "%"
		cursor = conn.cursor()
		cursor.execute("select * from Product where ProductId like '%s' order by ProductName ASC " % pid)
		result = cursor.fetchall()

		return render(request, 'billsearch.html', {'getdata': result})


def SearchProductByNameForBill(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pn = request.POST.get('SearchName')
		pn = pn + "%"
		cursor = conn.cursor()
		cursor.execute("select * from Product where ProductName like '%s' order by ProductName ASC " % pn)
		result = cursor.fetchall()

		return render(request, 'billsearch.html', {'getdata': result})


def DisplayInvForBill(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		pid = request.POST.get('SearchId')
		pid = pid + "%"
		cursor = conn.cursor()
		cursor.execute("select * from inventory where ProductId like '%s' order by ExpiryDate ASC " % pid)
		result = cursor.fetchall()

		return render(request, 'invdisplayforbill.html', {'getInv': result})


def AddInvToCart(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		Inid = request.POST.get('InvId')
		InQu = request.POST.get('InvQuan')
		InQu = int(InQu)
		cursor = conn.cursor()
		cursor.execute("select * from Inventory where InventoryId='%s'" % Inid)
		inv = cursor.fetchone()
		cursor.execute("select * from Product where ProductId='%s'" % inv.ProductId)
		pr = cursor.fetchone()
		price = int(pr.SalePerUnit) * InQu
		cursor.execute("Insert into Bill values ('%s','%s','%s','%s','%s','%s',getdate())" % (
			pr.ProductId, pr.ProductName, inv.InventoryId, InQu, price, inv.ExpiryDate))
		cursor.commit()
		finalQuantity = inv.Quantity - InQu
		cursor.execute("Update Inventory set Quantity='%s' where InventoryId = '%s'" % (finalQuantity, Inid))
		cursor.commit()
		cursor.execute("select * from Bill")
		cartlist = cursor.fetchall()
		return render(request, 'cart.html', {'ProList': cartlist})


def RemoveFromCart(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		Bid = request.POST.get('BillId')

		cursor = conn.cursor()
		cursor.execute("select * from Bill where BillId = '%s'" % Bid)
		b = cursor.fetchone()
		cursor.execute(
			"update Inventory set Inventory.Quantity = Inventory.Quantity +'%s' where InventoryId = '%s'" % (
				b.Quantity, b.InventoryId))
		cursor.commit()
		cursor.execute("delete from Bill where BillId='%s'" % Bid)
		cursor.commit()
		cursor.execute("select * from Bill")
		cartlist = cursor.fetchall()
		return render(request, 'cart.html', {'ProList': cartlist})


def TotalBill(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	cursor = conn.cursor()
	cursor.execute("select * from bill")
	result = cursor.fetchall()
	grandtotal = 0
	for r in result:
		grandtotal = grandtotal + int(r.Price)
	print(grandtotal)
	return HttpResponse(grandtotal)


def SaveBill(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		Cid = request.POST.get('CustId')
		cursor = conn.cursor()
		cursor.execute("Select * from sale")
		lastrow = cursor.fetchall()
		temp = 1
		for last in lastrow:
			temp = int(last.SaleId) + 1

		cursor.execute("select * from bill")
		curBill = cursor.fetchall()
		for oneBill in curBill:
			cursor.execute("insert into sale values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
				temp, Cid, oneBill.ProductId, oneBill.ProductName, oneBill.InventoryId, oneBill.Quantity, oneBill.Price,
				oneBill.ExpiryDate, oneBill.SaleDate))
			cursor.commit()
		cursor.execute("truncate table bill")
		cursor.commit()
		return HttpResponse("")


def Report(request):
	conn = pyodbc.connect('Driver={SQL Server};'
						  'Server=DESKTOP-SS1P55G\SQLEXPRESS;'
						  'Database=PMSDATABASE;'
						  'Trusted_Connection=yes;')
	if request.method == 'POST':
		FromDate = request.POST.get('FromDate')
		ToDate = request.POST.get('ToDate')
		cursor = conn.cursor()
		cursor.execute(
			"select ProductId, ProductName, Sum(Quantity) AS TotalQuantity , Sum(Price) AS TotalAmount from SALE where BillDate <='%s' and BillDate>='%s' group by ProductId, ProductName" % (
				ToDate, FromDate))
		result = cursor.fetchall()
		return render(request, 'reportlist.html', {'List': result})

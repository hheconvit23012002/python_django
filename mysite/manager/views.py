

import calendar
import datetime
from calendar import monthrange
from venv import create
from django.http import HttpRequest
from django.http import JsonResponse
from django.db.models import Sum,Count
from django.db.models import F,Q
from django.db.models.functions import ExtractMonth,ExtractDay
from django.shortcuts import redirect, render
from manager.models import *
from home.models import *
from django.core.files.storage import FileSystemStorage
# Create your views here.
def index(request):
    if 'name' in request.session:
        del request.session['name']
    if 'id' in request.session:
        del request.session['id']
    if 'admin' in request.session:
        del request.session['admin']
    return render(request,'pagesAdmin/home.html')
def addProduct(request):
    if 'admin' not in request.session:
        return redirect('/manager/')
    else:
        return render(request,'pagesAdmin/addProduct.html')
def procesAddProduct(request):
    if 'admin' not in request.session:
        return JsonResponse({"error": "That Bai"}, status=400)
    else:
        if request.is_ajax and request.method == 'POST' and request.FILES['photo'] :
            model = products()
            model.name = request.POST.get('name')
            my_file = request.FILES['photo']
            fs = FileSystemStorage()
            file_name = fs.save(my_file.name,my_file)
            model.photo = file_name
            model.desc = request.POST.get('description')
            model.price = request.POST.get('price')
            try:
                model.save()
                return JsonResponse({"instance": "Thanh cong"}, status=200)
            except:
                return JsonResponse({"error": "That Bai"}, status=400)
        return JsonResponse({"error": "That Bai"}, status=400)
def listProduct(request):
    if 'admin' not in request.session:
        return redirect('/manager/')
    else:
        if 'search'  in request.GET :
            searchText = ""
            searchText=request.GET.get('search')
            data = products.objects.filter(name__icontains = searchText)
            if(len(data)==0) :
                return render(request,'pagesAdmin/listProduct.html',{'messenger':"chua co san pham"})
            else : 
                return render(request,'pagesAdmin/listProduct.html',{'data':data,'search':searchText})
        else:
            data=products.objects.all()
            if(len(data)==0) :
                return render(request,'pagesAdmin/listProduct.html',{'messenger':"chua co san pham"})
            else : 
                return render(request,'pagesAdmin/listProduct.html',{'data':data})
        # try:
        # except:
        #     return render(request,'pagesAdmin/listProduct.html',{'messenger':"chua co san pham"})
def processDelete(request):
    if 'admin' not in request.session:
        return redirect('/manager/')
    else:
        if request.method == "GET":
            id = request.GET.get("id")
            try:
                products.objects.get(id=id).delete()
                return redirect('/manager/managerProduct/')
            except:
                return redirect('/manager/managerProduct/')



def UpdateProduct(request):
    if 'admin' not in request.session:
        return redirect('/manager/')
    else:
        if request.method == "GET":
            id = request.GET.get("id")
            try:
                data = products.objects.get(id=id)
                return render(request,"pagesAdmin/managerUpdate.html",{'data':data})
            except:
                return redirect('/manager/managerProduct/')

def processUpdate(request):
    if 'admin' not in request.session:
        return redirect('/manager/')
    else:
        if request.method == "POST":
            id = request.POST.get("id")
            name = request.POST.get('name')
            my_file = request.FILES
            if len(my_file) > 0:
                my_file = request.FILES['photo_new']
                fs = FileSystemStorage()
                file_name = fs.save(my_file.name,my_file)
            else :
                file_name= request.POST.get('photo_old')
            photo = file_name
            desc = request.POST.get('description')
            price = request.POST.get('price')
            try:
                products.objects.filter(id=id).update(name=name,photo=photo,desc=desc,price=price)
                return redirect('/manager/managerProduct/')
            except:
                return redirect('/manager/managerProduct/')

def login(request):
    if 'name' in request.session:
        del request.session['name']
    if 'id' in request.session:
        del request.session['id']
    if request.method == 'POST' :
        usn = request.POST.get('email')
        psw = request.POST.get('psw')
        try:
            data = manager.objects.get(email=usn)
            if data.password != psw:
                error = "sai tai khooan hoac mat khau"
                return render(request, 'pagesAdmin/login.html',{'error':error})
            else:
                request.session['name'] = data.name
                request.session['id'] = data.id
                request.session['admin']='1'
                return redirect('/manager/managerProduct/')
                # return render(request,'shop/shop.html',{'name' : data.name})
        except:
            error = "sai tai khooan hoac mat khau"
            return render(request, 'pagesAdmin/login.html',{'error':error})
            # return redirect('/login')
    else: return render(request, 'pagesAdmin/login.html')

def logout(request):
    if request.session['name'] and request.session['id'] and request.session['admin']:
        del request.session['name']
        del request.session['id']
        del request.session['admin']
        return redirect('/manager/')


def managerCheckOut(request):
    if 'admin' not in request.session:
        return redirect('/manager/')
    else:
        data = order.objects.all()
        if(len(data)==0) :
            return render(request,'pagesAdmin/listOrder.html',{'messenger':"chua co hoa don"})
        else : 
            return render(request,'pagesAdmin/listOrder.html',{'data':data})

def viewDetailOrder(request):
    if 'admin' not in request.session:
        return redirect('/')
    else:
        if request.method == 'GET':
            id = request.GET.get('id')
            data = order_product.objects.filter(id_order_id = id)
            sumPrice = 0
            for x in data:
                sumPrice += x.quantity*x.id_product.price
            return render(request,'pagesAdmin/viewDetailOrder.html',{'data':data,'sumPrice':sumPrice})

def actionOrder(request):
    if 'admin' not in request.session:
        return redirect('/')
    else:
        if request.method == 'GET':
            id = request.GET.get('id')
            typeAT = request.GET.get('type')
            if typeAT == 'ac':
                order.objects.filter(id=id).update(status=1)
            else:
                order.objects.filter(id=id).update(status=-1)
        return redirect('/manager/managerCheckout/')

def statisticalWeek(request):
    if 'admin' not in request.session:
        return redirect('/')
    else:
        now = datetime.datetime.now()
        day_current = now.strftime("%d")
        max_day = 7
        arr={}
        start_day_last_month = 32
        last_month = int(now.strftime("%m"))-1
        last_month_day = monthrange(2022,last_month)[1]
        if int(day_current) < max_day:
            get_day_last_month = max_day - int(day_current)
            start_day_last_month = last_month_day - get_day_last_month
            for i in range(start_day_last_month,last_month_day+1):
                key = str(i) + "_" + str(last_month)
                arr[key] = 0
            start_day_this_month =1
        else:
            start_day_this_month =int(day_current) - max_day
        for i in range(start_day_this_month,int(day_current)+1):
                key = str(i) + "_" + str(last_month+1)
                arr[key] = 0
        data = order.objects.values(
            'create_at__month',
            'create_at__day').annotate(
                ngay=ExtractDay('create_at'),
                thang=ExtractMonth('create_at'),
                doanh_thu=Sum('sum_price')).filter(Q(create_at__month=int(now.strftime("%m"))-1,
                create_at__day__gte = start_day_last_month,
                create_at__day__lte=last_month_day) | Q(create_at__month=int(now.strftime("%m")),
                create_at__day__gte = start_day_this_month,
                create_at__day__lte=day_current)).filter(status=1,create_at__year = 2022)
        
        for i in data:
            key = str(i.get('ngay')) + "_" + str(i.get('thang'))
            arr[key] = int(i.get('doanh_thu'))
        arrx=[]
        arry=[]
        for i in arr:
            arrx.append(str(i))
            arry.append(arr[i])
        return render(request,'pagesAdmin/charts.html',{'datax':arrx,'datay':arry})


def statisticalYear(request):
    if 'admin' not in request.session:
        return redirect('/')
    else:
        data = order.objects.values('create_at__month').annotate(thang=ExtractMonth('create_at') ,
        bills = Count(ExtractMonth('create_at'))).filter(create_at__month__gte = 1,
        create_at__month__lte =12,create_at__year=2022)
        arr =[]
        for i in range(1,13):
            value_thang=0
            key = calendar.month_name[i]
            for x in data:
                tmp_thang = int(x.get('thang'))
                if i == tmp_thang:
                    value_thang= int(x.get('bills'))
                    break
            arr.append([key,value_thang])
        return render(request,'pagesAdmin/charts2.html',{"data":arr})


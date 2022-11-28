from math import ceil
from django.db.models import Sum,Count
from django.http import JsonResponse
from distutils.log import error
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render,redirect
from requests import session
from django.core.files.storage import FileSystemStorage
from home.models import *
from datetime import datetime
# Create your views here.
def index(request):
    if 'admin' in request.session:
        del request.session['admin']
        if 'name' in request.session:
            del request.session['name']
        if 'id' in request.session:
            del request.session['id']
    return render(request,'pages/home.html')

def shop(request):
    if 'name' not in request.session:
        return redirect('/')
    else : 
        page_curent = 1
        sum_prodcut = products.objects.count()
        num_prodcut_one_page = 9
        num_page = ceil(sum_prodcut/num_prodcut_one_page)
        num_page_arr=[]
        for i in range(1,num_page+1):
            num_page_arr.append(i)
        if 'page' in request.GET:
            page_curent = int(request.GET.get('page'))
        if 'search'  in request.GET :
            searchText = ""
            searchText=request.GET.get('search')
            sum_prodcut = products.objects.filter(name__icontains = searchText).count()
            num_page = ceil(sum_prodcut/num_prodcut_one_page)
            num_page_arr=[]
            for i in range(1,num_page+1):
                num_page_arr.append(i)
            data = products.objects.filter(name__icontains = searchText)[(page_curent-1)*num_prodcut_one_page:(page_curent-1)*num_prodcut_one_page+num_prodcut_one_page]
            if(len(data)==0) :
                return render(request,'shop/shop.html',{'messenger':"chua co san pham"})
            else : 
                return render(request,'shop/shop.html',{'data':data,'search':searchText,'num_page':num_page_arr})
        else:
            
            data = products.objects.all()[(page_curent-1)*num_prodcut_one_page:(page_curent-1)*num_prodcut_one_page+num_prodcut_one_page]
            if(len(data)==0) :
                return render(request,'shop/shop.html',{'messenger':"chua co san pham"})
            else : 
                return render(request,'shop/shop.html',{'data':data,'num_page':num_page_arr})
def signup(request):
    if request.method == 'POST' :
        model = customers()
        model.name = request.POST.get('name')
        model.email = request.POST.get('email')
        model.password = request.POST.get('psw')
        model.phone_customer = request.POST.get('phone')
        model.address_customer = request.POST.get('address')
        # response = HttpResponse()
        # response.write(model.name)
        # return response
        try:
            model.save()
            return redirect('/')
        except:
            error = "email da ton tai"
            return render(request, 'pages/signup.html', { 'error': error})
            # return redirect('/login')
    else: return render(request,'pages/signup.html')
	
# def send_email(request, template_Url, subject_text, dataContent): 
#     # send email
#     template = render_to_string(template_Url, dataContent)

#     email = EmailMultiAlternatives(
#         subject_text,
#         strip_tags(template),
#         settings.EMAIL_HOST_USER,
#         [request.user.email],
#     )

#     email.attach_alternative(template, "text/html")
#     email.fail_silently = False
#     email.send()
	
def login(request):
    if 'name' in request.session:
        del request.session['name']
    if 'id' in request.session:
        del request.session['id']
    if 'admin' in request.session:
        del request.session['admin']
    if request.method == 'POST' :
        usn = request.POST.get('email')
        psw = request.POST.get('psw')
        try:
            data = customers.objects.get(email=usn)
            if data.password != psw:
                error ="sai pass"
                return render(request, 'pages/login.html', { 'error': error})
            else:
                request.session['name'] = data.name
                request.session['id'] = data.id
                return redirect('/shop')
                # return render(request,'shop/shop.html',{'name' : data.name})
        except:
            error = "khong ton tai email"
            return render(request, 'pages/login.html', { 'error': error})
            # return redirect('/login')
    else: return render(request,'pages/login.html')
def logout(request):
    if request.session['name'] and request.session['id']:
        del request.session['name']
        del request.session['id']
        return redirect('/')
def productDetail(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        if request.method == 'GET':
                id = request.GET.get('ID')
                if 'cmt' in request.GET and 'rating' in request.GET:
                    try:
                        model = rating_product()
                        model.cmt = request.GET.get('cmt')
                        model.rating = request.GET.get('rating')
                        model.id_customer_id = request.session.get('id')
                        model.id_product_id =id
                        model.save()
                    except:
                        rating_product.objects.filter(id_customer_id =request.session.get('id'),id_product_id=id).update(cmt=request.GET.get('cmt'),rating = request.GET.get('rating'))
                data = products.objects.get(id=id)
                rating_cmt = rating_product.objects.filter(id_product = id)
                sum=float(0)
                avg=0
                if len(rating_cmt) !=0:
                    for i in rating_cmt:
                        sum=sum+i.rating
                    avg = sum/len(rating_cmt)
                return render(request, 'shop/productDetail.html', { 'data': data,'rating_cmt':rating_cmt,'avg':avg})
            # try:
            # except:
            #     return redirect('/shop/')


def addToCart(request):
    if 'name' not in request.session:
        return JsonResponse({"error": "That Bai"}, status=400)
    else :
        if request.method =='GET':
            id_product = request.GET.get('id')
            id_user = request.session.get('id')
            try:
                data = cart.objects.get(id_product_id = id_product , id_customer_id = id_user)
                data.quantity +=1
                cart.objects.filter(id_product_id = id_product , id_customer_id = id_user).update(quantity = data.quantity)
            except:
                model = cart()
                model.id_customer_id = id_user
                model.id_product_id = id_product
                model.quantity = 1
                model.save()
        return JsonResponse({"instance": "Thanh cong"}, status=200)

def viewCart(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        id = request.session.get('id')
        if request.method == 'POST':
            try:
                data = cart.objects.filter(id_customer_id = id)
                model = order()
                model.id_customer_id = id
                model.name_recerver = request.POST.get('name_receiver')
                model.phone_recerver = request.POST.get('phone_receiver')
                model.address_recerver = request.POST.get('address_receiver')
                model.status = 0
                model.sum_price = float(request.POST.get('sum_price'))
                if model.name_recerver =='' and model.phone_recerver =='' and model.address_recerver == '' and len(data) ==0:
                    return redirect('/shop/viewcart/')
                else:
                    model.save()
                    
                    for x in data:
                        model2 = order_product()
                        model2.id_order_id = order.objects.order_by('id').last().id
                        model2.id_product_id = x.id_product.id
                        model2.quantity = x.quantity
                        model2.save()
                    cart.objects.filter(id_customer_id = id).delete()
                    return redirect('/shop/')
            except:
                return redirect('/shop/viewcart/')
        else:
            try:
                data = cart.objects.filter(id_customer_id = id)
                receiver = customers.objects.get(id=id)
                sumPrice = 0
                for x in data:
                    sumPrice += x.quantity*x.id_product.price
                return render(request,'shop/viewCart.html',{'data':data,'sumPrice':sumPrice,'receiver':receiver})
            except:
                return redirect('/shop')
def viewReceipt(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        id = request.session.get('id')
        data = order.objects.filter(id_customer_id = id )
        return render(request,'shop/viewCheckOut.html',{'data':data})


def viewDetailOrder(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        if request.method == 'GET':
            id = request.GET.get('id')
            data = order_product.objects.filter(id_order_id = id)
            sumPrice = 0
            for x in data:
                sumPrice += x.quantity*x.id_product.price
            return render(request,'shop/viewDetailOrder.html',{'data':data,'sumPrice':sumPrice})

# def checkout(request):
#     if 'name' not in request.session:
#         return redirect('/')
#     else:
#         if request.method == 'POST':
#             id = request.session.get('id')
#             try:
#                 data = cart.objects.filter(id_customer_id = id)
#                 model = order()
#                 model.id_customer = id
#                 model.name_recerver = request.POST.get('name_receiver')
#                 model.phone_recerver = request.POST.get('phone_receiver')
#                 model.address_recerver = request.POST.get('address_receiver')
#                 model.status = 0
#                 model.sum_price = request.POST.get('sum_price')
#                 if model.name_recerver =='' and model.phone_recerver =='' and model.address_recerver == '':
#                     return redirect('/shop/viewcart/')
#                 else:
#                     model.save()
#                     order_product.id_order = order.objects.order_by('id').first()
#                     for x in data:
#                         order_product.id_product = x.id_product.id
#                         order_product.quantity = x.quantity
#                         order_product.save()
#                     cart.objects.filter(id_customer_id = id).delete()
#                     return redirect('/shop/')
#             except:
#                 return redirect('/shop/viewcart/')

                
def changeQuantity(request):
    if 'name' not in request.session:
        return JsonResponse({"error": "That Bai"}, status=400)
    else:
        id = request.GET.get('id')
        type = request.GET.get('type')
        data = cart.objects.get(id_product_id=id)
        if type == 'incre' :
            cart.objects.filter(id_product_id=id).update(quantity= data.quantity+1)
        else:
            if data.quantity ==1 :
                cart.objects.filter(id_product_id=id).delete()
            else:
                cart.objects.filter(id_product_id=id).update(quantity= data.quantity-1)
        return JsonResponse({"instance": "Thanh cong"}, status=200)

def deleteInCart(request):
    if 'name' not in request.session:
        return JsonResponse({"error": "That Bai"}, status=400)
    else:
        id = request.GET.get('id')
        cart.objects.filter(id_product_id=id).delete()
        return JsonResponse({"instance": "Thanh cong"}, status=200)

def info(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        id = request.session.get('id')
        data = customers.objects.get(id=id)
        return render(request,'shop/info.html',{'data':data})
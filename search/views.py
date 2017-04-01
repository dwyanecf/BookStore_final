from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
import MySQLdb
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from django.db.models import Max, Min
from django import forms
from models import Admin,Authors,BlackList,Book,BookAuthors,BookTypes,Comments,OrderItems,\
Orders,UserInfo,LineItem,Cart
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib

category_list=BookTypes.objects.all()
#form
class UserForm(forms.Form): 
    username = forms.CharField(label='Username',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
class UserResisterForm(forms.Form): 
    username = forms.CharField(label='Username',max_length=30, min_length=3)
    password = forms.CharField(label='Password',widget=forms.PasswordInput(),max_length=30, min_length=4)
    repassword = forms.CharField(label='Repeat Password',widget=forms.PasswordInput(),max_length=30, min_length=4)
    email = forms.EmailField(label='Email',max_length=50, min_length=8)


    #form
class UserUpdateForm(forms.Form): 

    pwd = forms.CharField(label='Old Password',widget=forms.PasswordInput(),max_length=30, min_length=4)  # Field name made lowercase.
    new_pwd = forms.CharField(label='New Password',widget=forms.PasswordInput(),max_length=30, min_length=4)
    repassword = forms.CharField(label='Repeat New',widget=forms.PasswordInput(),max_length=30, min_length=4)
    address = forms.CharField(label='ADDRESS', max_length=200)  # Field name made lowercase.
    phone = forms.CharField(label='PHONE', max_length=10)  # Field name made lowercase.
    email = forms.EmailField(label='Email',max_length=50, min_length=8)
def make_password(password):
    assert password
    hash = hashlib.md5(password).hexdigest()
    return hash

def check_password(hash, password):
    generated_hash = make_password(password)
    return hash == generated_hash
#Register
@csrf_exempt
def regist(req):
    if req.method == 'POST':
        uf = UserResisterForm(req.POST)
        if uf.is_valid():
            #get form input
            username = uf.cleaned_data['username']
            password = make_password(uf.cleaned_data['password'])
            repassword = make_password(uf.cleaned_data['repassword'])
            email = uf.cleaned_data['email']
            
            if repassword!=password:
                error_msg='The passwords do not match!'
                return render_to_response('register.html', {'uf':uf,'error_msg': error_msg})
            user=UserInfo.objects.filter(user_id__exact = username)
            if user:
                error_msg='Username has been taken!'
                return render_to_response('register.html', {'uf':uf,'error_msg': error_msg})
            else:
                #add to db
                UserInfo.objects.create(user_id= username,pwd=password,email=email)
                return HttpResponseRedirect('/regist_success/')
    else:
        uf = UserResisterForm()
    return render_to_response('register.html',{'uf':uf}, context_instance=RequestContext(req))

#login
@csrf_exempt
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #get username and pwd from user input
            username = uf.cleaned_data['username']
            password = make_password(uf.cleaned_data['password'])
            #validate
            user = UserInfo.objects.filter(user_id__exact = username,pwd__exact = password)
            if user:
                req.session['username'] = username
                #user found,go to index
                response = HttpResponseRedirect('/home/')
                #write username into cookie,valid for 3600
                response.set_cookie('username',username,3600)
                return response
            else:
                error_msg='Username do not match password!'
                return render_to_response('login.html', {'uf':uf,'error_msg': error_msg})
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))
    
def getFeaturedBooksList():
    featured_books_list=[]
    for x in range (0,4):
        random_idx = random.randint(0, Book.objects.count()/100)
        featured_books_list.append(Book.objects.all()[random_idx])
    return featured_books_list
def getNewBooksList():
    new_books_list=[]
    for x in range (0,4):
        random_idx = random.randint(0, Book.objects.count()/100)
        new_books_list.append(Book.objects.all()[random_idx])
    return new_books_list
def home(req):
    cart = req.session.get("cart",None)
    if not cart:
        cart = Cart()
    req.session["cart"] = cart
    username = req.COOKIES.get('username','')
    featured_books_list=getFeaturedBooksList()
    new_books_list=getNewBooksList()
    best_sellers_list=Book.objects.annotate(best_seller=Min('quantity'))[:4]
    category_list=BookTypes.objects.all()
    return render(req,'home.html' ,{'username':username,'featured_books_list': featured_books_list,'new_books_list':new_books_list,'best_sellers_list':best_sellers_list,'category_list':category_list})
def regist_success(req):
    return render_to_response('regist_success.html')
#log out
def logout(req):
    response = HttpResponseRedirect('/home/')
    #delete username in cookie
    response.delete_cookie('username')
    req.session['username']=''
    return response
@csrf_exempt
def SearchBook(req):
    if 'category' in req.GET:
        category=int(req.GET['category'])
        if not category:
            category=int(req.REQUEST['category'])
        result_list=Book.objects.filter(type__exact=category)
        category_record=BookTypes.objects.filter(type_id__exact=category)[0]
    if 'keyword' in req.GET:
        keyword=req.GET['keyword']
        if not keyword:
            keyword=req.REQUEST['keyword']
        result_list=Book.objects.filter((Q(isbn__icontains =keyword)|Q(title__icontains=keyword))&Q(is_available__exact="yes"))
#        result=Book.objects.filter(Q(isbn__icontains =keyword)|Q(title__icontains=keyword)\
#        |Q(type__icontains=keyword)|Q(isbn__icontains=keyword))
            #only selects data from book, no join at present
    paginator = Paginator(result_list, 9) # Show 25 contacts per page
    page = req.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    if 'keyword' in req.GET:
        return render(req, 'searchresult.html', {'results': results,'keyword':keyword,'category_list':category_list})
    if 'category' in req.GET:
        return render(req, 'searchresult.html', {'results': results,'category':category,'category_record':category_record,'category_list':category_list})
#shopping cart
def view_cart(request):
    cart = request.session.get("cart",None)
    t = get_template('shoppingcart.html')
    category_list=BookTypes.objects.all()
    if not cart:
        cart = Cart()
    request.session["cart"] = cart
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c), {'category_list':category_list})
#    return render(request, 'shoppingcart.html')
def add(request):
    isbn=request.GET['isbn']
    product = Book.objects.get(isbn__exact = isbn)
    cart = request.session.get("cart",None)
    if not cart:
        cart = Cart()
        request.session["cart"] = cart
    cart.add_product(product)
    request.session['cart'] = cart
    return view_cart(request)#
def show(request):
    cart = Cart(request.session)
    response = ''
    category_list=BookTypes.objects.all()
    for item in cart.items:
        response += '%(quantity)s %(item)s for $%(price)s\n' % {
            'quantity': item.quantity,
            'item': item.product.name,
            'price': item.subtotal,
        }
        response += 'items count: %s\n' % cart.count
        response += 'unique count: %s\n' % cart.unique_count
#    return HttpResponse(response)
    return render(request, 'shoppingcart.html',{'category_list':category_list})
def remove_item(request):
    isbn=request.GET['isbn']
    product = Book.objects.get(isbn__exact = isbn)
    cart = request.session.get("cart",None)
    cart.remove_product(product)
    request.session['cart'] = cart
    return view_cart(request)
def change_item_quantity(request):
    isbn=0
    product =[]
    quantity=-1;
    if 'quantity_change_add' in request.GET:
        quantity=1;
        isbn=request.GET['quantity_change_add']
        product = Book.objects.get(isbn__exact = isbn)
    else:
         isbn=request.GET['quantity_change_minus']
         product = Book.objects.get(isbn__exact = isbn)
    cart = request.session.get("cart",None)
    cart.change_item_quantity(product,quantity)
    request.session['cart'] = cart
    return view_cart(request)
def clean_cart(request):
    request.session['cart'] = Cart()
    return view_cart(request)
def CheckOut(request):
    return render(request,'checkout.html',{'category_list':category_list})
def SubmitOrder(request):
    user_id=request.session.get('username','')
    if not user_id:
        message='Please log in first!'
        return render(request,'login.html',{'category_list':category_list})
    
    order_date=datetime.datetime.now()
    ship_address=request.GET['shipping_address']
    ship_phone=request.GET['contact_phone']
    cart = request.session.get("cart",None)
    total_price=cart.total_price
    message=request.GET['message']
    order=Orders(user_id=user_id,order_date=order_date,ship_address=ship_address,\
                 ship_phone=ship_phone,total_price=total_price,message=message,is_available="yes")
    order.save()
    order_id=Orders.objects.only('order_id').latest('order_id').order_id
    for item in cart.items:
        item_isbn=item.product.isbn
        book=Book.objects.get(isbn=item_isbn)
        quantity=item.quantity
        order_items=OrderItems(order_id=order_id,isbn=book,quantity=quantity)
        order_items.save()
    request.session['cart'] = Cart()
    return render(request,'checkoutsuccess.html',{'category_list':category_list})
def set_quantity(request):
    cart = Cart(request.session)
    product = Book.objects.get(isbn__exact=request.POST.get('isbn'))
    quantity = request.POST.get('quantity')
    cart.set_quantity(product, quantity)
    return HttpResponse()

def myorder(req):
    username = req.COOKIES.get('username','')
    orders = Orders.objects.filter(Q(user__user_id__exact =username)&Q(is_available__exact="yes"))
    result_list = OrderItems.objects.filter(order=orders.values('order_id'))
   
    paginator = Paginator(result_list, 5) # Show 5 contacts per page
    page = req.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(req, 'myorder.html', {'username':username, 'results': results, 'orders': orders,'category_list':category_list})
def remove_order(request):
#    return render(request,'home.html' )
    orderid=request.GET['orderid']
    Orders.objects.filter(order_id__exact = orderid).update(is_available="no")
    return myorder(request)
    
@csrf_exempt
def profile(req):
    username = req.session.get('username')
    if req.method == 'POST':
        uf = UserUpdateForm(req.POST)
        if uf.is_valid():
            #get form input
            
            pwd = make_password(uf.cleaned_data['pwd'])
            new_pwd = make_password(uf.cleaned_data['new_pwd'])
            repassword = make_password(uf.cleaned_data['repassword'])
            address =uf.cleaned_data['address']
            phone = uf.cleaned_data['phone']
            email = uf.cleaned_data['email']

            user = UserInfo.objects.filter(user_id__exact = username,pwd__exact = pwd)
            if user:
                if new_pwd!=repassword:
                    error_msg='The new passwords do not match!'
                    return render_to_response('profile.html', {'uf':uf,'error_msg': error_msg})
                else:
                     t = UserInfo.objects.get(user_id= username)
                     t.pwd = repassword
                     t.address =address
                     t.phone =phone
                     t.email =email
                     t.save()
                     error_msg='Update success !'
                     return render_to_response('profile.html', {'uf':uf,'error_msg': error_msg})


            else:
                error_msg='password does not match !'
                return render_to_response('profile.html', {'uf':uf,'error_msg': error_msg})

               
    else:
        uf = UserUpdateForm()
    return render_to_response('profile.html',{'uf':uf}, context_instance=RequestContext(req))
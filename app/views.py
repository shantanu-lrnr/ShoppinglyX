from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self,request):
        mobiles = Product.objects.filter(category='M').order_by('?')
        laptops = Product.objects.filter(category='L').order_by('?')
        topwears = Product.objects.filter(category='TW').order_by('?')
        bottomwears = Product.objects.filter(category='BW').order_by('?')
        return render(request, 'app/home.html',{'mobiles':mobiles,'topwears':topwears,'bottomwears':bottomwears,'laptops':laptops})

class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        product.description_points = product.description.split('|')
        discount = product.selling_price - product.discounted_price
        # Calculate the percentage discount
        percentage_off = (discount / product.selling_price) * 100
        product_available = False
        print(request.user)
        if request.user.is_authenticated:
          product_available = Cart.objects.filter(user=request.user,product=product).exists()
        return render(request, 'app/productdetail.html',{'product':product,'product_available':product_available,'product.description_points':product.description_points,'percentage_off':percentage_off})

@login_required    
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  Cart(user=user,product = product).save()
  return redirect('showcart')

@login_required
def show_cart(request):
  carts = Cart.objects.filter(user=request.user)
  amount  = 0.0
  shipping_amount = 70.0
  totalamount=0.0
  user_cart_list = Cart.objects.filter(user=request.user)
  if user_cart_list:
    for p in user_cart_list:
      amount = amount + p.product.discounted_price*p.quantity
    totalamount = shipping_amount+amount
    return render(request, 'app/addtocart.html',{'carts':carts,'totalamount':totalamount,'amount':amount})
  else:
    return render(request,'app/empty_cart.html')
  
def plus_cart(request):
  prod_id = request.GET['prod_id']
  product = Product.objects.get(id=prod_id)
  cart = Cart.objects.get(Q(product=product) & Q(user=request.user))
  cart.quantity+=1
  cart.save()
  amount  = 0.0
  shipping_amount = 70.0
  user_cart_list = Cart.objects.filter(user=request.user)
  for p in user_cart_list:
    amount = amount + p.product.discounted_price*p.quantity
  totalamount = shipping_amount+amount

  data = {
    'quantity':cart.quantity,
    'amount':amount,
    'totalamount':totalamount
  }
  return JsonResponse(data)

def minus_cart(request):
  prod_id = request.GET['prod_id']
  product = Product.objects.get(id=prod_id)
  cart = Cart.objects.get(Q(product=product) & Q(user=request.user))
  cart.quantity-=1
  cart.save()
  amount  = 0.0
  shipping_amount = 70.0
  user_cart_list = Cart.objects.filter(user=request.user)
  for p in user_cart_list:
    amount = amount + p.product.discounted_price*p.quantity
  totalamount = shipping_amount+amount

  data = {
    'quantity':cart.quantity,
    'amount':amount,
    'totalamount':totalamount
  }
  return JsonResponse(data)

def remove_cart(request):
  prod_id = request.GET['prod_id']
  product = Product.objects.get(id=prod_id)
  cart = Cart.objects.get(Q(product=product) & Q(user=request.user))
  cart.delete()
  amount  = 0.0
  shipping_amount = 70.0
  user_cart_list = Cart.objects.filter(user=request.user)
  for p in user_cart_list:
    amount = amount + p.product.discounted_price*p.quantity
  totalamount = shipping_amount+amount

  data = {
    'amount':amount,
    'totalamount':totalamount
  }
  return JsonResponse(data)


def buy_now(request,pk):
  user = request.user
  product = Product.objects.get(id=pk)
  Cart(user=user,product = product).save()
  return redirect('checkout')


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

def mobile(request,data=None):
 print(data)
 if data==None:
   mobiles = Product.objects.filter(category='M')

 elif data=='Redmi' or data=='Samsung' or data=='Iphone' or data=='Oneplus' or data == 'Realme':
   mobiles = Product.objects.filter(category='M').filter(brand=data)

 elif data=='below':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)

 elif data=='above':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
   
 return render(request, 'app/mobile.html',{'mobiles':mobiles,'data':data})

def laptop(request,data=None):
 if data==None:
   laptops = Product.objects.filter(category='L')

 elif data=='Dell' or data=='Hp' or data=='Acer':
   laptops = Product.objects.filter(category='L').filter(brand=data)

 elif data=='below':
   laptops = Product.objects.filter(category='L').filter(discounted_price__lt=30000)

 elif data=='above':
   laptops = Product.objects.filter(category='L').filter(discounted_price__gt=30000)
   
 return render(request, 'app/laptop.html',{'laptops':laptops,'data':data})

def top_wear(request,data=None):
 if data==None:
   topwears = Product.objects.filter(category='TW')

 elif data=='Vanheusen' or data=='Levis' or data=='Allensolly':
   topwears = Product.objects.filter(category='TW').filter(brand=data)

 elif data=='below':
   topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=2000)

 elif data=='above':
   topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=2000)
   
 return render(request, 'app/top_wear.html',{'topwears':topwears,'data':data})

def bottom_wear(request,data=None):
 if data==None:
   bottomwears = Product.objects.filter(category='BW')

 elif data=='Nike' or data=='Lyra' or data=='Pepe':
   bottomwears = Product.objects.filter(category='BW').filter(brand=data)

 elif data=='below':
   bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=2000)

 elif data=='above':
   bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=2000)
   
 return render(request, 'app/bottom_wear.html',{'bottomwears':bottomwears,'data':data})


class CustomerRegistrationView(View):
  def get(self,request):
    form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html',{'form':form})

  def post(self,request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request,'Congratulations!! Registered Successfully')
      form.save()
    return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    if not add:
      messages.error(request,'Please add the address before placing an order')
      return redirect('profile')
    cart_items = Cart.objects.filter(user=user)
    amount  = 0.0
    shipping_amount = 70.0
    totalamount=0.0
    cart_product = Cart.objects.filter(user=request.user)
    if cart_product:
        for p in cart_product:
            amount = amount + p.product.discounted_price*p.quantity
        totalamount = shipping_amount+amount
        return render(request, 'app/checkout.html',{'add':add,'cart_items':cart_items,'totalamount':totalamount})
    return render(request,'app/empty_cart.html')

@login_required
def payment_done(request):
  user = request.user
  customer_id = request.GET.get('custid')
  customer = Customer.objects.get(id=customer_id)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect('orders')


def search(request):
  query = request.GET.get('data','')
  data = query.replace(' ','').capitalize()
  print(data)
  if not data:
    return redirect('/')
  elif data in ['Redmi','Samsung','Iphone','Oneplus','Realme']: 
    return redirect(f'/mobile/{data}/')
  elif data in ['Acer','Dell','Hp']:
    return redirect(f'/laptop/{data}/')
  elif data in [' Nike','Lyra','Pepe']:
    return redirect(f'/bottomwear/{data}/')
  elif data in ['Levis','Vanheusen','Allensolly']:
    return redirect(f'/topwear/{data}/')
  else:
    return render(request,'app/search_not_found.html')



@method_decorator(login_required,name="dispatch")
class ProfileView(View):
  def get(self,request):
    form = CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      zipcode = form.cleaned_data['zipcode']
      state = form.cleaned_data['state']
      customer = Customer(user=request.user,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
      customer.save()
      messages.success(request,'Profile Updated Successfully!!')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    

from typing import Any
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from ecommapp.models import Products,Carts,PlaceOrder,Address,Categories
from ecommapp.form import SignInForm,SignUpForm,CartForm,PlaceOrderForm
from django.db.models import Count
from django.views import View
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView,CreateView,ListView,DetailView,UpdateView,DeleteView
# Create your views here.

class Home(View):
    # template_name='index.html'
    
    # def get_context_data(self,request, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = request.user
    #     products = Products.objects.all()
    #     context['products'] = products
    #     address = Address.objects.filter(user=user)
    #     context['address'] = address
    #     return context
    
    def get(self,request,*args,**kwargs):
        user = request.user
        products=Products.objects.all()
        category = Categories.objects.all()
        if user.is_authenticated:
            address = Address.objects.filter(user=user)
            count = Carts.objects.filter(user_id=request.user,status="in-cart").count()
            return render(request,'index.html',{'products':products,'address':address,'categories':category,"c":count})
        else:
            return render(request,'index.html',{'products':products,'categories':category})


class SignUpView(CreateView):
    template_name='register.html'
    model=User
    form_class=SignUpForm
    success_url=reverse_lazy('home')
        
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=SignInForm()
        return render(request,'signin.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=SignInForm(request.POST)
        if form.is_valid():
            u=form.cleaned_data.get("username")
            p=form.cleaned_data.get("password")
            user=authenticate(request,username=u,password=p)
            if user:
                login(request,user)
                messages.success(request,"Login Successfull")
                return redirect('home')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('signin')
            
            
            
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"Logout Successfull")
        return redirect('home')
    
    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        category = Categories.objects.all()
        return render(request,'detail.html',{'product':product,'categories':category})    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        user=request.user
        count=request.POST.get("count")
        if count:
            Carts.objects.create(user=user,product=product,quantity=count)
        return redirect("home")
    # model=Products
    # template_name='detail.html'
    # pk_url_kwarg='id'
    # context_object_name='product'
    
    
class CartCreateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        category = Categories.objects.all()
        return render(request,'cart.html',{'product':product,'categories':category})
        
class CartListView(View):
    def get(self,request,*args,**kwargs):
        user=request.user
        cart=Carts.objects.filter(user=user,status='in-cart')
        sum = Carts.objects.filter(user=user,status='in-cart').aggregate(total=Sum('quantity'))['total']
        tot = Carts.objects.filter(user=user,status='in-cart')
        total = 0
        for i in tot:
            total +=(i.quantity*i.product.price)
        address = Address.objects.filter(user=user)
        category = Categories.objects.all()
        count = Carts.objects.filter(user_id=request.user,status="in-cart").count()
        return render(request,'cartlist.html',{'cartlist':cart,'address':address,'sum':sum,'total':total,'categories':category,'c':count})
    
class CartDelete(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        Carts.objects.get(id=id).delete()
        return redirect('list')
    
class AdrressView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        address = request.POST.get("address")
        Address.objects.create(user=user,address=address)
        return redirect("home")
    
class DeleteAdrressView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Address.objects.get(id=id).delete()
        return redirect("home")
    
    
class PlaceOrderView(View):
    def post(self,request,*args,**kwargs):
       cart_id=kwargs.get("id") 
       cart=Carts.objects.get(id=cart_id)
       product=Products.objects.get(id=cart.product.id)
       user=request.user
       address=request.POST.get('address')
       quantity = ((product.quantity)-(cart.quantity))
       PlaceOrder.objects.create(user=user,product=product,address=address)
       cart.status='order-placed'
       cart.save()
       product.quantity = quantity
       product.save()
       return redirect('home')
        

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        category = Categories.objects.get(id=id)
        products = Products.objects.filter(category=category)
        categories = Categories.objects.all()
        return render(request,'category.html',{'products':products,'category':category,'categories':categories})
    
    
class SearchView(View):
    def post(self, request, *args, **kwargs):
        pro = request.POST.get("product")
        product_name = Products.objects.filter(product_name = pro)
        product = product_name[0]
        return render(request,'detail.html',{'product':product})
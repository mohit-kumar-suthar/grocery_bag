from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import product_form,login,register,otp
from .models import product
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate,login as Login,logout
from django.contrib import messages

# Create your views here.

def add_view(request):
    if not request.user.is_authenticated:
        messages.error(request,'Content not accessible plz login first')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    first_name = request.user.first_name
    form = product_form()
    if request.method == 'POST':
        form = product_form(request.POST)
        if form.is_valid():
            form.name = form.cleaned_data['name']
            form.quantity = form.cleaned_data['quantity']
            form.status = form.cleaned_data['status']
            form.save()
            return redirect('index')
    return render(request,'add.html',{'add':form,'first_name':first_name})

def index_view(request):
    try:
        first_name = request.user.first_name
    except:
        first_name = False
    pro_obj = product.objects.all()
    return render(request,'index.html',{'datas':pro_obj,'first_name':first_name})

def delete_view(request,pk):
    if not request.user.is_authenticated:
        messages.error(request,'Content not accessible plz login first')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    pro_obj = product.objects.get(pk=pk)
    pro_obj.delete()
    return redirect('index')

def update_view(request,pk):
    if not request.user.is_authenticated:
        messages.error(request,'Content not accessible plz login first')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    first_name = request.user.first_name
    pro_obj = product.objects.get(pk=pk)
    form = product_form(initial={'name':pro_obj.name,'quantity':pro_obj.quantity,'status':pro_obj.status})
    if request.method == 'POST':
        form = product_form(request.POST)
        if form.is_valid():
            pro_obj.name = form.cleaned_data['name']
            pro_obj.quantity = form.cleaned_data['quantity']
            pro_obj.status = form.cleaned_data['status']
            pro_obj.save()
            return redirect('index')
    return render(request, 'update.html',{'update':form,'first_name':first_name})

def filter_view(request):
    if not request.user.is_authenticated:
        messages.error(request,'Content not accessible plz login first')
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    first_name = request.user.first_name
    if request.method == 'POST':
        pro_obj = product.objects.filter(created_at=request.POST['date'])
        return render(request,'index.html',{'datas':pro_obj,'first_name':first_name})
    return redirect('index')

def login_view(request):
    form = login()
    if request.method == 'POST':
        form = login(request.POST)
        if form.is_valid():      
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,username=email,password=password)
            if not User.objects.filter(username=email).exists():
                messages.error(request, 'The user does not exist')
                return redirect('login')
            if user is not None:
                Login(request,user)
                return redirect('index')
            messages.error(request, 'Incorrect password. Please try again!')
            return redirect('login')
    return render(request,'login.html',{'login_form':form})

def register_view(request):
    form = register()
    if request.method == 'POST':
        form = register(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            otp =  send_otp(email)
            request.session['user'] = [first_name, last_name, email, password,otp]
            request.session.set_expiry(60)
            return redirect('otp')
    return render(request,'register.html',{'register_form':form})
             
def otp_view(request):
    if request.session.get('user'):
        form = otp()
        if request.method == 'POST':
            form = otp(request.POST)
            if form.is_valid():
                otp_num = form.cleaned_data['otp_num']
                user=request.session.get('user')
                if int(user[4]) == int(otp_num):
                    user = User.objects.create_user(
                    username = user[2], 
                    first_name = user[0],
                    last_name = user[1],
                    password = user[3],
                    is_active = True, )   
                    del request.session['user']    
                    messages.info(request, 'Account created Successfully')
                    return redirect('login')
                else:
                    messages.error(request, 'enter valid OTP')
                    return render(request,'otp.html',{'otp_form':form})
                return redirect('home')
        return render(request,'otp.html',{'otp_form':form})
    return redirect('register')

def send_otp(email):
    try:
        otp = random.randint(0000000,999999)
        send_mail(
        'One Time Password from Grocery Bag',
        'Your OTP is '+str(otp)+' and session expire in 60 seconds',
        'teamfirecode.project@gmail.com',
        [email],
        fail_silently=False,
        )

        return otp
    except:
        return 'Internet Connection failed'

def logout_view(request):
    logout(request)
    messages.info(request,'Logged out')
    return redirect('login')
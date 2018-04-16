from django.shortcuts import render, redirect
from django.http import JsonResponse

from rrsite.models import CustomUser, Restaurant, Photo, Review
from rrsite.util.string import username_type, valid_email, valid_phone
from RRWeb.settings import EMAIL_LOGIN_METHOD, PHONE_LOGIN_METHOD, PHOTO_STATIC_URL_FORMAT
from rrsite.auth.email import *
from rrsite.auth.phone import *


# Create your views here.
def index(request):
    return render(request, 'rrsite/index.html')


def login(request):
    # 如果是GET或HEAD请求，返回渲染登录页面
    if request.method == 'GET' or request.method == "HEAD":
        return render(request, 'rrsite/login.html')
    # 如果是POST请求，处理表单内容
    elif request.method == 'POST':
        # 获取用户名、密码参数
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        login_method = username_type(username)
        # 登录账号/密码错误信息
        error_login_msg = {'msg': 'Email(Phone Number) or Password Incorrect, Please Check Again'}
        # 登录格式错误信息
        error_format_msg = {'msg': 'Email(Phone Number) Format Incorrect, Please Check Again'}
        # 根据不同登录方式进行登录操作
        # 邮箱登录
        if login_method == EMAIL_LOGIN_METHOD:
            user = CustomUser.objects.filter(email__iexact=username, password__exact=password)
            if user:
                # 将用户名和登录方式存入session实现自动登录机制
                request.session['username'] = username
                request.session['login_method'] = login_method
                # 登录成功，跳转到主页
                return redirect('/')
            else:
                # 账号/密码错误重新渲染页面，返回错误信息
                return render(request, 'rrsite/login.html', context=error_login_msg)
        # 手机号登录
        elif login_method == PHONE_LOGIN_METHOD:
            user = CustomUser.objects.filter(phone__exact=username, password__exact=password)
            if user:
                # 将用户名和登录方式存入session实现自动登录机制
                request.session['username'] = username
                request.session['login_method'] = login_method
                # 登录成功，跳转到主页
                return redirect('/')
            else:
                # 账号/密码错误重新渲染页面，返回错误信息
                return render(request, 'rrsite/login.html', context=error_login_msg)
        else:
            # 账号格式错误重新渲染页面，返回错误信息
            return render(request, 'rrsite/login.html', context=error_format_msg)


def register_view(request):
    if request.method == 'GET' or request.method == 'HEAD':
        return render(request, 'rrsite/register.html')


def register_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        error_email_format = {'error_email_msg': 'Your Email \'s Format is Incorrect'}
        if email is None or password is None or confirm_password is None:
            return render(request, 'rrsite/register.html', context=error_email_format)
        error_send_email = {'msg': 'Sending Authentication Email Failed. Please Check Your Email'}
        register_success_msg = {'msg': 'Email Register Success! Please Check Your Email '
                                       'and Activate the Account ASAP! You Can Login Now'}
        if valid_email(email):
            if send_register_email(email) == 1:
                user = CustomUser.objects.create(email=email, password=password, is_superuser=0, is_staff=0,
                                                 is_active=1, last_login=datetime.now()
                                                 , date_joined=datetime.now())
                user.save()
                return render(request, 'rrsite/login.html', context=register_success_msg)
            else:
                return render(request, 'rrsite/register.html', context=error_send_email)
        else:
            return render(request, 'rrsite/register.html', context=error_email_format)
    else:
        return redirect('/register')


def register_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', None)
        code = request.POST.get('code', None)
        password = request.POST.get('password', None)
        error_phone_format = {'error_phone_msg': 'Your Phone \'s Format is Incorrect'}
        error_send_phone = {'error_phone_msg': 'Your Phone \'s Format is Incorrect'}
        register_success_msg = {'msg': 'Phone Register Success! You Can Login Now!'}
        if valid_phone(phone):
            if check_phone_code(phone, code):
                user = CustomUser.objects.create(phone=phone, password=password, is_superuser=0, is_staff=0, is_active=1
                                                 , last_login=datetime.now(), date_joined=datetime.now())
                user.save()
                return render(request, 'rrsite/login.html', context=register_success_msg)
            else:
                return render(request, 'rrsite/register.html', context=error_send_phone)
        else:
            return render(request, 'rrsite/register.html', context=error_phone_format)
    else:
        return redirect('/register')


def recommend_restaurant(request):
    if request.method == 'GET':
        category = request.GET.get('category', None)
        if category is not None or category != '':
            category = str(category).replace('_', ' ')
            restaurants_values_list = list(Restaurant.objects
                                           .filter(category__category__iexact=category, review_count__gte=400).order_by('?')[:6].values())
            for restaurants_dict in restaurants_values_list:
                photo_id = Photo.objects.filter(restaurant_id=restaurants_dict.get('id', None)).order_by('?')[0].id
                restaurants_dict['photo_url'] = PHOTO_STATIC_URL_FORMAT.format(photo_id)
            return JsonResponse({'msg': '请求成功', 'code': 1, 'data': restaurants_values_list})
        else:
            return JsonResponse({'msg': '传入类别信息为空', 'code': 0, 'data': []})
    else:
        return JsonResponse({'msg': '请求方法错误', 'code': -1, 'data': []})


def forgetpassword(request):
    return render(request, 'rrsite/forgetpassword.html')



def email_activation(request):
    return render(request, 'rrsite/emailactivation.html')

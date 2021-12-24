import razorpay
import smtplib
import socket
import requests
from email.message import EmailMessage
import json
from .forms import MyForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.orders import Order
from .models.customer import Customer
from .models.sellproduct import SellProduct
from .models.feedback import Feedback
from .models.video import Video
from .models.sellings import Sellings
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from book_store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)


def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
        error_message = 'First Name Required'
    elif len(customer.first_name) < 4:
        error_message = 'First Name must be 4 characters long or more'
    elif not customer.last_name:
        error_message = 'last Name Required'
    elif len(customer.last_name) < 4:
        error_message = 'Last Name must be 4 characters long or more'
    elif not customer.phone:
        error_message = 'Phone Number Required'
    elif len(customer.phone) < 10:
        error_message = 'Phone Number must be 10 characters long'
    elif not customer.password:
        error_message = 'Password Required'
    elif customer.password != customer.confirm:
        error_message = 'Passwords do not match'
    elif len(customer.password) < 8:
        error_message = 'Password must be 8 characters long'
    elif not customer.email:
        error_message = 'Email Required'
    elif len(customer.email) < 5:
        error_message = 'Enter valid email'
    elif customer.isExists():
        error_message = 'Email Address already exists'

    return error_message


def registerUser(request):
    postData = request.POST
    first_name = postData.get('first_name')
    last_name = postData.get('last_name')
    phone = postData.get('phone')
    address = postData.get('address')
    city = postData.get('city')
    landmark = postData.get('landmark')
    pin = postData.get('pin')
    email = postData.get('email')
    password = postData.get('password')
    confirm = postData.get('confirm')

    # recaptcha stuf
    '''
    clientKey = request.POST['g-recaptcha-response']
    secretKey = "6LdXLRkbAAAAAAIQIQ-1G4QKQHa5SRtugMzAUX1z"
    captchaData = {
        'secret': secretKey,
        'response': clientKey,
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
    response = json.loads(r.text)
    verify = response['success']
    print('your success is:', verify)
    '''
    ca = request.POST["g-recaptcha-response"]
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': "6LdXLRkbAAAAAAIQIQ-1G4QKQHa5SRtugMzAUX1z",
        'response': ca,
        'remoteip': get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    status = verify_rs.get("success", False)
    print(status)
    if not status:
        HttpResponse('Failed')
    # validation
    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'city': city,
        'pin': pin,
        'landmark': landmark,
        'email': email,

    }
    error_message = None
    customer = Customer(first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        address=address,
                        city=city,
                        landmark=landmark,
                        pin=pin,
                        email=email,
                        password=password,
                        confirm=confirm)
    error_message = validateCustomer(customer)

    # saving
    if not error_message:
        customer.password = make_password(customer.password)
        customer.confirm = make_password(customer.confirm)
        customer.register()
        return redirect('login')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'signup.html', data)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


'''
class Shop(View):
    def get(self, request):
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are:', request.session.get('email'))
        return render(request, 'shop.html', data)

    def post(self,request):
        product = request.POST.get('product')
        print(product)
'''
def home(request):
    request.session['cart'] = {}
    return redirect('shop')

def shop(request):
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        stocks = request.GET.get('stock')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are:', request.session.get('email'))
        return render(request, 'shop.html', data)
    else:
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        stocks = request.GET.get('stock')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('shop')


def single(request, my_id):
    product = Product.objects.filter(id=my_id)
    print(product)
    return render(request, 'single_product.html', {'product': product[0]})


# login class

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('shop')
            else:
                error_message = 'Email or password is invalid!!'
        else:
            error_message = 'Email or password is invalid!!'
        return render(request, 'login.html', {'error': error_message})


'''
def login(request):
    if request.method == 'GET':
        return  render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('shop')
            else:
                error_message = 'Email or password is invalid!!'
        else:
            error_message = 'Email or password is invalid!!'

        return render(request, 'login.html', {'error' : error_message})
'''


def about(request):
    video = Video.objects.all()
    return render(request, 'about.html', {'video': video})





'''
def checkout(request):
    return render(request, 'cart.html')
'''

'''
def pay(request):
    if request.method == 'POST':
        amount = 50000
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_KdlxhmSFnMeKQi','yb2xzxg53q1tjdXibCd1bhWi'))
        payment = client.order.create({'amount':amount , 'currency':'INR', 'payment_capture':'1'})
    return render(request, 'payment.html')
'''


@csrf_exempt
def success(request):
    email_id = "kavyagoudar8@gmail.com"
    email_pass = "mkavya@20"
    msg = EmailMessage()
    msg['Subject'] = "Order Confirmation from Boomerang Books"
    msg['from'] = email_id
    msg['to'] = "kavyagoudar8@gmail.com"
    msg.set_content("Your order has been placed.Keep Buying.Keep Reading.Thankyou")
    files = ['invoice.pdf']
    for file in files:
        with open(file, 'rb') as m:
            file_data = m.read()
            file_name = m.name
        msg.add_attachment(file_data, maintype='image', subtype='octet-stream', filename=file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)
    cart = request.session.get('cart')
    products = Product.get_products_by_id(list(cart.keys()))
    '''server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("kavyagoudar8@gmail.com", "mkavya@20")
    server.sendmail("bookbiz@gmail.com", "kavyagoudar8@gmail.com",
                    "Your order has been placed.Keep Buying.Keep Reading.Thankyou")
    server.quit()
    # request.session['cart'] = {}'''
    return render(request, 'summary.html', {'products': products})


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        customerID = request.session.get('email')
        value = Customer.get_customer_by_email(customerID)
        # id = Order.objects.all
        # value = Order.objects.all
        # print(products)
        return render(request, 'cart.html', {'products': products, 'values': value})

    def post(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        customerID = request.session.get('email')
        value = Customer.get_customer_by_email(customerID)
        # id = request.session.get('order')

        # print(products)
        return render(request, 'cart.html', {'products': products, 'values': value})


class Cart1(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        print(product)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)  # removes item when it is 0 in cart
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('cart')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        # print(products)
        return render(request, 'cart.html', {'products': products})


class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        mode = request.POST.get('mode')
        pin = request.POST.get('pin')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        value = {
            'address': address,
            'phone': phone,
            'landmark': landmark,
            'city': city,
            'pin': pin
        }
        data = {
            'values': value
        }
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          landmark=landmark,
                          city=city,
                          mode=mode,
                          pin=pin,
                          quantity=cart.get(str(product.id))
                          )
            order.save()
        orders = Order.get_orders_by_customer(customer)
        if mode == 'Cash On Delivery':
            email_id = "kavyagoudar8@gmail.com"
            email_pass = "mkavya@20"
            msg = EmailMessage()
            msg['Subject'] = "Order Confirmation from Boomerang Books"
            msg['from'] = email_id
            msg['to'] = "kavyagoudar8@gmail.com"
            msg.set_content("Your order has been placed.Keep Buying.Keep Reading.Thankyou")
            files = ['invoice.pdf']
            for file in files:
                with open(file,'rb') as m:
                    file_data = m.read()
                    file_name = m.name
                msg.add_attachment(file_data,maintype='image',subtype='octet-stream',filename=file_name)
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(email_id,email_pass)
                smtp.send_message(msg)
            '''socket.getaddrinfo('localhost', 8080)
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("kavyagoudar8@gmail.com", "mkavya@20")

            server.sendmail("bookbiz@gmail.com", "kavyagoudar8@gmail.com",
                            "Your order has been placed.Keep Buying.Keep Reading.Thankyou")
            server.quit()'''
            # request.session['cart'] = {}
            return render(request, 'summary.html', {'products': products})

        else:
            # request.session['cart'] = {}
            amount = 50000
            order_currency = 'INR'
            client = razorpay.Client(auth=('rzp_test_KdlxhmSFnMeKQi', 'yb2xzxg53q1tjdXibCd1bhWi'))
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

            return render(request, 'payment.html')


class Orders(View):

    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)

        return render(request, 'orders.html', {'orders': orders})


def sell(request):
    if request.method == 'GET':
        return render(request, 'sell.html')
    else:
        postData = request.POST
        name = postData.get('name')
        category = postData.get('category')
        front_image = postData.get('front_image')
        index_image = postData.get('index_image')
        back_image = postData.get('back_image')
        author = postData.get('author')
        edition = postData.get('edition')
        description = postData.get('description')
        price = postData.get('price')
        phone = postData.get('phone')
        page = postData.get('page')
        publisher = postData.get('publisher')
        address = postData.get('address')
        city = postData.get('city')
        pin = postData.get('pin')
        state = postData.get('state')
        customer = request.session.get('customer')
        sellproducts = SellProduct(customer=Customer(id=customer),
                                   name=name,
                                   category=category,
                                   front_image=front_image,
                                   index_image=index_image,
                                   back_image=back_image,
                                   author=author,
                                   edition=edition,
                                   description=description,
                                   price=price,
                                   phone=phone,
                                   page=page,
                                   publisher=publisher,
                                   address=address,
                                   city=city,
                                   state=state,
                                   pin=pin)
        sellproducts.reg()
        print(customer, sellproducts)
        return render(request, 'sell.html')


class SellView(View):
    def get(self, request):
        customer = request.session.get('customer')
        sell = SellProduct.get_sellings_by_customer(customer)
        print(sell)

        return render(request, 'sell_view.html', {'sell': sell})


'''
def Image(request):
    if request.method == 'GET':
        return render(request, 'sellings.html')
    else:
        postData = request.POST
        f_image = postData.get('f_image')
        m_image = postData.get('m_image')
        b_image = postData.get('b_image')
        image = Sellings( f_image=f_image,
                       m_image=m_image,
                       b_image=b_image,
        )
        image.register()
        return render(request,'sellings.html')'''


def feedback(request):
    if request.method == 'GET':
        return render(request, 'feedback.html')
    else:
        postData = request.POST
        title = postData.get('title')
        description = postData.get('description')
        customer = request.session.get('customer')
        quality = postData.get('quality')
        exp = postData.get('exp')
        feedbacks = Feedback(customer=Customer(id=customer),
                             title=title,
                             description=description,
                             quality=quality,
                             exp=exp)

        feedbacks.reg()
        print(customer, feedbacks)
        return render(request, 'feedback.html')


'''
def current(request):
    r = requests.get('https://get.geojs.io/')
    print(r)
    ip_requests = requests.get('https://get.geojs.io/v1/ip.json')
    ipadd = ip_requests.json()['ip']
    print(ipadd)

    url = 'https://get.geojs.io/v1/ip/geo/'+ipadd+'.json'
    geo_request = requests.get(url)
    geo_data = geo_request.json()
    print(geo_data)
    print(geo_data['latitude'])
'''


def forgot(request):
    return render(request, 'password_reset.html')


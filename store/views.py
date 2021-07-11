from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import Product
from .models import Category
from .models import Customer
from .models import Order


from .middilewares.auth import auth_middleware
from django.views import View



# Create your views here.



class index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
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
        return redirect('index')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        # print(products)

        categories = Category.get_all_category()
        categoryId = request.GET.get('category')
        if categoryId:
            products = Product.get_all_product_category_id(categoryId)
        else:
            products = Product.get_all_products()
        data = {}
        data['product'] = products
        data['category'] = categories
        print(request.session.get('email'))
        return render(request, 'index.html', data)


class signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postdata = request.POST
        first_name = postdata.get('firstname')
        last_name = postdata.get('lastname')
        email = postdata.get('email')
        phone = postdata.get('phone')
        password = postdata.get('password')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,

        }

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            password=password)

        error_message = self.validateCustomer(customer)

        # submitting

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect("index")
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required"
        elif customer.first_name:
            if len(customer.first_name) < 4:
                error_message = "First Name must be atleast 4 character"
        elif not customer.last_name:
            error_message = "Last Name Required"

        elif len(customer.last_name) < 4:
            error_message = "First Name must be atleast 4 character"

        elif not customer.phone:
            error_message = "Mobile number required"

        elif len(customer.phone) < 10:
            error_message = "Mobile number atlest 10 number"
        elif len(customer.password) < 6:
            error_message = "password must be 6 char long"

        elif len(customer.email) < 5:
            error_message = "Email must be 5 character long"

        elif Customer().isExists():
            error_message = "Email is Already Taken..."

        return error_message


class Login(View):
    return_url=None
    def get(self, request):
        Login.return_url=request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = Customer.Customer_get_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)

                else:
                   Login.return_url=None
                   return redirect("index")
            else:
                error_message = "Invalid Email and Password"
        else:
            error_message = "Invalid Email and Password"

        return render(request, 'login.html', {
            'error': error_message
        })


class Logout(View):
    def get(self, request):
        request.session.clear()
        return redirect('login')


class cart(View):

    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_id(ids)
        print(products)
        return render(request, "cart.html", {'products': products})


class checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_id(list(cart.keys()))

        for product in products:
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))

            order.save()
        request.session['cart'] = {}

        print(address, phone, customer)
        return redirect('cart')


class order(View):
  
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_order_by_customer(customer)

        print(orders)
        orders=orders.reverse()
        return render(request, 'orders.html',{'orders':orders})




def otp(request):
    return render(request,'otp.html')
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Customer, Product,Order,OrderItem,ShippingAddress
import datetime

def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
    else:
        order={'total_items':0}
    context = {'products':products,'order':order}
    return render(request, "store/store.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items=[]
        order={'total_items':0,'final_price':0}
    context = {'items':items, 'order':order}
    return render(request, "store/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items=[]
        order={'total_items':0,'final_price':0}
    context = {'items':items, 'order':order}
    return render(request, "store/checkout.html",context)

from django.views.decorators.csrf import csrf_exempt

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    # print(f" orderitem={orderItem} \n created={created}")


    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse("this is my data", safe=False)


@csrf_exempt
def submitpaymet(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.final_price:
            order.complete = True
        order.save()

        if order.complete == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
                country= data['shipping']['country'],
            )
    else:
        print("user is not login")

    return JsonResponse("this is my data", safe=False)

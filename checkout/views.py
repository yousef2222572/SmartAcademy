import json

import stripe
from academy_core import models as academy_models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from checkout.forms import UserInfoForm, MyPayPalPaymentsForm
from checkout.models import Transaction, PaymentMethod

from django.core.mail import send_mail
import math
from django.conf import settings
from django.utils.translation import gettext as _
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse




# def make_order(request):
#     if request.method != 'POST':
#         return redirect('store.checkout')

#     form = UserInfoForm(request.POST)

#     if form.is_valid():
#         cart = Cart.objects.filter(session=request.session.session_key).last()
#         products = Product.objects.filter(pk__in=cart.items)

#         total = 0
#         for item in products:
#             total += item.price

#         if total <= 0:
#             return redirect('store.checkout')

#         order = Order.objects.create( 
#             customer=form.cleaned_data,
#             total=total,
#         )

#         for product in products:
#             order.orderproduct_set.create(
#                 product_id=product.id,
#                 price=product.price,
#             )
#         send_order_email(order, products)

#         Cart.objects.filter(session=request.session.session_key).delete()

#         return redirect('store.checkout_complete')

#     else:
#         return redirect('store.checkout')



def make_transaction(request,pm,course_id):
    
    form = UserInfoForm(request.POST)

    if form.is_valid():

        course = academy_models.Courses.objects.filter(pk=course_id).first()

        print("course_id:", course_id)
        print("course:", course)

        total = course.price


        if total <= 0:
            return None
        

        return  Transaction.objects.create(
            user=request.user,
            customer = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': form.cleaned_data['phone_number'],
            },
            payment_method=pm,
            items=course.id,
            amount=math.ceil(total),
            
            
        )
    else:
        return redirect('academy.checkout')

def stripe_config(request):
    #  هذا المفتاح لست بحاجة ل تشفيره بما انه مفتاح عام 
    return JsonResponse({
        'public_key' : "i removed"
    })


def stripe_transaction(request):
    stripe.api_key = "i remove"
    course_id = '18'
    account = stripe.Account.retrieve()
    print("Django Stripe account:", account.id)
    transaction = make_transaction(request,PaymentMethod.Stripe,course_id)
    if not transaction:
        return JsonResponse({
            'message' : _("please enter a valid information.")
        },status=400)
        
    stripe.api_key = "i remove"
    
    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency = 'USD',
        payment_method_types=['card'],
        metadata={
            'transaction':transaction.id,
        }
        
    )
    print(intent['client_secret'])
    
    return JsonResponse({
        'client_secret' : intent['client_secret'],  
        })
    



def paypal_transaction(request):
    transaction = make_transaction(request,PaymentMethod.Paypal)
    if not transaction:
            
        return JsonResponse({
            'message' : _("please enter a valid information.")
        },status=400)
        
        
    form=MyPayPalPaymentsForm(initial={
        'business':settings.PAYPAL_EMAIL,
        'amount':transaction.amount,
        'invoice':transaction.id,
        'currency_code':settings.CURRENCY,  
        'return_url' :f'http://{request.get_host()}{reverse("academy.checkout_complete")}',
        'cancel_url' :f'http://{request.get_host()}{reverse("academy.checkout")}',
        'notify_url' :f'http://{request.get_host()}{reverse("checkout.paypal-webhook")}',
        
    })
    return HttpResponse(form.render())



def send_order_email(order, products):
    msg_html = render_to_string('emails/order.html', {
        'order': order,
        'products': products,
    })

    send_mail(
        subject='Order Completed',
        html_message=msg_html,
        message=msg_html,
        from_email= 'no-replay@example.com',
        recipient_list= [order.customer['email']],
    )
    


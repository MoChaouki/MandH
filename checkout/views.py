from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .checkout import Checkout
from cart.cart import Cart
from store.models import Product, Profile
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from store.forms import UserInfoForm, UpdateUserForm, CheckoutForm
import paypalrestsdk
from store.models import Customer


paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "AcArGLlr2osY_RHsZzxiD5iyWRV-EppFCo21ErngvJk1770HDR1iph-88PXeZfEtaXHEhxrM5xI1bTgR", # Updated
    "client_secret": "EGT-bKpJVTRUXRwlelt9DliPepT_woefIlHS01J8RxI8JoU9rysd65A9AP1tVCWX4vggfQFHPACkLe48", # Updated
})

def checkout_summary(request): 
    cart = Cart(request)
    # Fix the method call to get products
    cart_products = cart.get_prods()  # Fixed: Call the method
    quantities = cart.get_quants()  # Also ensure this is called as a method
    totals = cart.cart_total()

    # Fetch current user's profile
    current_user = Profile.objects.get(user=request.user)
    user_form = UpdateUserForm(request.POST or None, instance=current_user.user)
    form = UserInfoForm(request.POST or None, instance=request.user.profile)
    checkout_form = CheckoutForm(request.POST or None)

    # Fetch product categories in the cart
    cart_categories = set([product.category for product in cart_products])

    # Fetch recommendations: 2 products per category, excluding products already in the cart
    recommended_products = []
    for category in cart_categories:
        recommendations = Product.objects.filter(category=category).exclude(id__in=[p.id for p in cart_products])[:2]
        recommended_products.extend(recommendations)

    context = {
        "form": form,
        "user_form": user_form,
        "checkout_form": checkout_form,
        "totals": totals,
        "quantities": quantities,
        "cart_products": cart_products,
        "recommended_products": recommended_products,  # Add recommendations to the context
    }
    return render(request, 'checkout.html', context)



def create_payment(request): 
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": request.POST.get('total_cmd'),  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })
	
    if payment.create():   
        customer_firstname = request.POST.get('customer_firstname')
        customer_lastname = request.POST.get('customer_lastname')
        customer_phone = request.POST.get('customer_phone')
        customer_mail = request.POST.get('customer_email')
        checkout_customer = Customer(
				first_name=customer_firstname,
				last_name=customer_lastname,
				phone=customer_phone,
				email=customer_mail,
				password=''
			)
        checkout_customer.save()
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')
    
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')



def payment_failed(request):
    return render(request, 'payment_failed.html')

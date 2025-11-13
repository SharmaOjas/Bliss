import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cart.models import Cart

@login_required
def checkout(request):
    """Handles Razorpay checkout for user's cart"""
    cart = Cart.objects.get(user=request.user)
    amount = int(cart.total_price * 100)  # Convert to paise
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "payments/checkout.html", {
        "payment": payment,
        "key": settings.RAZORPAY_KEY_ID,
        "total": cart.total_price,
    })

import json
import razorpay
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from cart.models import Cart, Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    amount = int(cart.total_price * 100)
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

@csrf_exempt
@login_required
def verify_payment(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid payload"}, status=400)

    required_keys = {"razorpay_order_id", "razorpay_payment_id", "razorpay_signature"}
    if not required_keys.issubset(set(data.keys())):
        return JsonResponse({"success": False, "error": "Missing fields"}, status=400)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"],
        })
    except Exception:
        return JsonResponse({"success": False, "error": "Signature verification failed"}, status=400)

    try:
        cart = Cart.objects.get(user=request.user)
        subtotal = Decimal(cart.total_price)
        tax = Decimal("0.00")
        shipping = Decimal("0.00")

        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            delivery_address="Not provided",
            status="confirmed",
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                recipe=cart_item.recipe,
                servings=cart_item.servings,
                quantity=cart_item.quantity,
                excluded_ingredients=','.join([str(ri.id) for ri in cart_item.excluded_ingredients.all()]),
                price=cart_item.customized_price,
            )

        cart.items.all().delete()
    except Exception:
        return JsonResponse({"success": False, "error": "Order creation failed"}, status=500)

    return JsonResponse({"success": True, "redirect_url": reverse("users:orders")})

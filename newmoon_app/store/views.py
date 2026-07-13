from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, SiteSetting, Category, CustomOrder, Order
from .cart import Cart
from .forms import CustomOrderForm

def home(request):
    site = SiteSetting.load(); featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
    lang = request.GET.get('lang', 'fa')
    for p in featured:
        if lang == 'en': p.display_name = p.name_en or p.name_fa
        elif lang == 'ar': p.display_name = p.name_ar or p.name_fa
        else: p.display_name = p.name_fa
    return render(request, "store/home.html", {"site": site, "featured": featured, "lang": lang})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})

def product_list(request):
    products = Product.objects.filter(is_active=True); return render(request, "store/product_list.html", {"products": products})

def cart_add(request, product_id):
    cart = Cart(request); product = get_object_or_404(Product, id=product_id)
    cart.add(product=product); messages.success(request, f"{product.name_fa} اضافه شد."); return redirect('store:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request); product = get_object_or_404(Product, id=product_id)
    cart.remove(product); return redirect('store:cart_detail')

def cart_detail(request):
    cart = Cart(request); return render(request, 'store/cart_detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0: return redirect('store:product_list')
    if request.method == 'POST':
        full_name = request.POST.get('full_name'); phone = request.POST.get('phone'); address = request.POST.get('address')
        order = Order.objects.create(full_name=full_name, phone=phone, address=address, total_price=cart.get_total_price())
        cart.clear()
        return render(request, "store/order_success.html", {"name": full_name, "order": order})
    return render(request, "store/checkout.html", {"cart": cart})

def custom_order_request(request):
    if request.method == "POST":
        form = CustomOrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(); messages.success(request, "درخواست ثبت شد."); return redirect('store:home')
    else: form = CustomOrderForm()
    return render(request, "store/custom_order.html", {"form": form})

def api_product_list(request):
    products = Product.objects.filter(is_active=True)
    data = [{"id": p.id, "title": p.name_fa, "price": p.price, "link": request.build_absolute_uri(p.get_absolute_url())} for p in products]
    return JsonResponse(data, safe=False)

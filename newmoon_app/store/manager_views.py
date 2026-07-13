from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from .models import Product, SiteSetting, CustomOrder
from .manager_forms import ProductForm, SiteSettingForm, CustomOrderResponseForm

# کنترل دسترسی مدیر
def is_staff_check(u): return u.is_authenticated and (u.is_staff or u.is_superuser)
staff_required = user_passes_test(is_staff_check, login_url="/manage/login/")

# ۱. پیشخوان (Dashboard)
@staff_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    new_orders = CustomOrder.objects.filter(status='pending').count()
    return render(request, "manager/dashboard.html", {"products": products, "new_orders": new_orders})

from .models import ProductImage # حتما این بالا باشد

@staff_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # ذخیره کردن تصاویر آلبوم (گالری)
            images = request.FILES.getlist('gallery_images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, "محصول سلطنتی با موفقیت ثبت شد.")
            return redirect("/manage/")
        else:
            # نمایش خطاهای فرم در صورت وجود
            for error in form.errors.values(): messages.error(request, error)
    return render(request, "manager/product_form.html", {"form": ProductForm(), "mode": "create"})

@staff_required
def product_edit(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=obj)
        if form.is_valid(): form.save(); return redirect("/manage/")
    return render(request, "manager/product_form.html", {"form": ProductForm(instance=obj), "obj": obj, "mode": "edit"})

@staff_required
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    obj.delete(); messages.warning(request, "حذف شد."); return redirect("/manage/")

# ۳. تنظیمات و سفارشات
@staff_required
def site_settings_edit(request):
    obj = SiteSetting.load()
    if request.method == "POST":
        form = SiteSettingForm(request.POST, request.FILES, instance=obj)
        if form.is_valid(): form.save(); return redirect("/manage/settings/")
    return render(request, "manager/site_settings.html", {"form": SiteSettingForm(instance=obj)})

@staff_required
def custom_order_list(request):
    orders = CustomOrder.objects.all().order_by('-created_at')
    return render(request, "manager/custom_orders.html", {"orders": orders})

@staff_required
def order_detail(request, pk):
    order = get_object_or_404(CustomOrder, pk=pk)
    if request.method == "POST":
        form = CustomOrderResponseForm(request.POST, request.FILES, instance=order)
        if form.is_valid(): order.status = 'quoted'; form.save(); return redirect("manager:custom_order_list")
    return render(request, "manager/order_detail.html", {"order": order, "form": CustomOrderResponseForm(instance=order)})

# ۴. احراز هویت
def manager_login(request):
    if request.method == "POST":
        u = request.POST.get("username"); p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user and user.is_staff: login(request, user); return redirect("/manage/")
    return render(request, "store/manager/login.html")

def manager_logout(request): logout(request); return redirect("/manage/login/")
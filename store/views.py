from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Category, Brand, Product, ContactMessage
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


def contacto(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        subject = (request.POST.get("subject") or "").strip()
        message = (request.POST.get("message") or "").strip()

        # Validación mínima del lado servidor
        if not all([name, email, subject, message]):
            messages.error(request, "Por favor completa todos los campos.")
        else:
            ContactMessage.objects.create(
                name=name, email=email, subject=subject, message=message
            )
            messages.success(request, "¡Gracias! Recibimos tu mensaje.")
            return redirect("contacto")

    return render(request, "store/contacto.html")


def ofertas(request):
    return render(request, 'store/ofertas.html')

def catalog_view(request):
    """
    Vista principal del catálogo.
    - Obtiene todos los productos activos de la base de datos.
    - Los pasa al template para mostrarlos en una tabla sencilla.
    """
    products = Product.objects.filter(is_active=True)
    return render(request, 'store/catalog.html', {'products': products})


def category_view(request, slug):
    """
    Muestra los productos filtrados por categoría.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'store/catalog.html', {
        'products': products,
        'selected_category': category.name
    })


def brand_view(request, slug):
    """
    Muestra los productos filtrados por marca.
    """
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand, is_active=True)
    return render(request, 'store/catalog.html', {
        'products': products,
        'selected_brand': brand.name
    })

def categories_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'store/categories.html', {'categories': categories})


def brands_list(request):
    brands = Brand.objects.all().order_by('name')
    return render(request, 'store/brands.html', {'brands': brands})

def product_detail(request, slug):
    """
    Muestra la información detallada de un producto individual.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': product})


def cart_view(request):
    cart = Cart(request)
    items = []
    for it in cart.cart.values():
      items.append({
        **it,
        'subtotal': float(it['price']) * int(it['quantity'])
      })
    context = {'cart_items': items, 'total': cart.get_total()}
    return render(request, 'store/cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        cart.add(product_id, name, price)
        return JsonResponse({'status': 'ok'})


@ensure_csrf_cookie
def ofertas(request):
    return render(request, 'store/ofertas.html')

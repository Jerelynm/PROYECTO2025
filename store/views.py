from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Category, Brand, Product, ContactMessage, Order
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
from django.db.models import F, Q

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


def catalog_view(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
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
    items, total = _cart_items_from_session(request)
    return render(request, 'store/cart.html', {'cart_items': items, 'total': total})

@csrf_exempt  # blindaje express para tu presentación
def add_to_cart(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'method-not-allowed'}, status=405)

    # Leer datos del POST
    pid   = (request.POST.get('id') or '').strip()
    name  = (request.POST.get('name') or '').strip()
    price = (request.POST.get('price') or '0').strip()
    qty   = (request.POST.get('qty') or '1').strip()

    # Sanitizar
    try:
        qty = max(1, int(qty))
    except:
        qty = 1

    # --- ESCRIBIR DIRECTO A LA SESIÓN (sin usar Cart) ---
    cart = request.session.get('cart', {}) or {}
    item = cart.get(pid, {'name': name, 'price': str(price), 'quantity': 0})
    item['name'] = name
    item['price'] = str(price)
    item['quantity'] = int(item.get('quantity', 0)) + qty
    cart[pid] = item
    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({'status': 'ok', 'count': len(cart)})



@ensure_csrf_cookie
def ofertas(request):
    # Entrega productos al template y deja la cookie CSRF lista
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'store/ofertas.html', {'products': products})


@require_POST
def cart_remove(request):
    cart = Cart(request)
    pid = request.POST.get('id')
    cart.remove(pid)
    # devolver estado actualizado también leyendo de sesión
    items, total = _cart_items_from_session(request)
    return JsonResponse({'ok': True, 'total': str(total), 'count': len(items)})

@require_POST
def cart_update(request):
    cart = Cart(request)
    pid = request.POST.get('id')
    qty = request.POST.get('qty', '1')
    cart.set_quantity(pid, qty)
    items, total = _cart_items_from_session(request)
    return JsonResponse({'ok': True, 'total': str(total), 'count': len(items)})


def checkout(request):
    # Usa tu helper que ya tienes
    items, total = _cart_items_from_session(request)

    if request.method == 'POST':
        # Normaliza items a tipos JSON-friendly
        items_json = []
        for it in items:
            items_json.append({
                'id': str(it['id']),
                'name': it['name'],
                'price': str(Decimal(it['price']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'quantity': int(it['quantity']),
                'subtotal': str(Decimal(it['subtotal']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            })

        order = Order.objects.create(
            customer_name=request.POST.get('name', ''),
            customer_email=request.POST.get('email', ''),
            shipping_address=request.POST.get('address', ''),
            items=items_json,
            total=Decimal(total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        )

        # Limpia carrito
        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'store/checkout_success.html', {
            'items': items,
            'total': total,
            'order_id': order.id,
        })

    # GET → muestra previo
    return render(request, 'store/checkout.html', {'items': items, 'total': total})



def _cart_items_from_session(request):
        """
        Lee el carrito directamente de la sesión y devuelve:
        - items: lista de dicts {id, name, price(Decimal), quantity(int), subtotal(Decimal)}
        - total: Decimal
        """
        raw = request.session.get('cart', {}) or {}
        items = []
        total = Decimal('0.00')
        for pid, it in raw.items():
            price = Decimal(str(it.get('price', '0')))
            qty = int(it.get('quantity', 0))
            sub = price * qty
            items.append({
                'id': pid,
                'name': it.get('name', ''),
                'price': price,
                'quantity': qty,
                'subtotal': sub
            })
            total += sub
        return items, total


def _to_decimal(val):
    """Convierte 'Q2,625.00' -> Decimal('2625.00') sin explotar."""
    if val is None:
        return Decimal('0')
    s = str(val).strip()
    s = s.replace(',', '.')                # coma a punto
    s = re.sub(r'[^\d\.]', '', s)          # quita Q, $, espacios, etc.
    if s.count('.') > 1:                   # si hay más de un punto, deja solo el primero
        i = s.find('.')
        s = s[:i+1] + s[i+1:].replace('.', '')
    try:
        return Decimal(s or '0')
    except InvalidOperation:
        return Decimal('0')

def _cart_items_from_session(request):
        raw = request.session.get('cart', {}) or {}
        items = []
        total = Decimal('0')
        for pid, it in raw.items():
            price = _to_decimal(it.get('price', '0'))
            qty = int(it.get('quantity') or 0)
            sub = (price * qty).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            items.append({
                'id': pid,
                'name': it.get('name', ''),
                'price': price,
                'quantity': qty,
                'subtotal': sub
            })
            total += sub
        total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return items, total



@csrf_exempt
def cart_clear_now(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart')
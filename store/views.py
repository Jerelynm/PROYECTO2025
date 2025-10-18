from django.shortcuts import render
from .models import Product

def catalog_view(request):
    """
    Vista principal del catálogo.
    - Obtiene todos los productos activos de la base de datos.
    - Los pasa al template para mostrarlos en una tabla sencilla.
    """
    products = Product.objects.filter(is_active=True)
    return render(request, 'store/catalog.html', {'products': products})
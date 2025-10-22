from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Category, Brand, Product

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



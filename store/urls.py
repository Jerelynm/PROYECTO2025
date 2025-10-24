from django.urls import path
from . import views

urlpatterns = [
    # Página principal del catálogo
    path('', views.catalog_view, name='catalog'),

    # Listas generales
    path('categories/', views.categories_list, name='categories'),
    path('brands/', views.brands_list, name='brands'),

    # Filtros por categoría y marca (usando slugs)
    path('category/<slug:slug>/', views.category_view, name='category_products'),
    path('brand/<slug:slug>/', views.brand_view, name='brand_products'),

    # Página de detalle de cada producto
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Nuevas vistas del grupo
    path('contacto/', views.contacto, name='contacto'),
    path('ofertas/', views.ofertas, name='ofertas'),
]

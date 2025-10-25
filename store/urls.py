from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('categories/', views.categories_list, name='categories'),
    path('brands/', views.brands_list, name='brands'),
    path('category/<slug:slug>/', views.category_view, name='category_products'),
    path('brand/<slug:slug>/', views.brand_view, name='brand_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contacto/', views.contacto, name='contacto'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

]
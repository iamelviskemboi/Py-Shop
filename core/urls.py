from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    # homepage
    path('', views.HomeView.as_view(), name='home'),

    # product
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),

    # cart
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/',
         views.remove_from_cart, name='remove-from-cart'),

    # checkout
    path('checkout/', views.checkout, name='checkout'),
]

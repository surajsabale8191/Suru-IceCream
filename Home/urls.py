from django.contrib import admin
from django.urls import path
from Home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ContactAPIView
# from .views import (
#     ProductListCreateAPIView,
#     ProductRetrieveUpdateDestroyAPIView
# )

urlpatterns = [
    
    path("", views.user_login, name='login'),
    path("home", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("services/", views.services, name='services'),
    path("contact/", views.contact, name='contact'),
    path("api/contact/", ContactAPIView.as_view(), name="contact-api"),
    path("registration", views.registration, name='registration'),
    path("login", views.user_login, name='login'),
    path("cart", views.cart, name='cart'),
    path('products/', views.products, name='products'),
    #path("api/products/", ProductListCreateAPIView.as_view(), name="product-list"),
    #path("api/products/<int:pk>/", ProductRetrieveUpdateDestroyAPIView.as_view(), name="product-detail"),

    path('add-to-cart/<int:icecream_id>/', views.add_to_cart, name='add_to_cart'),
    path(
    'increase/<int:cart_id>/',
    views.increase_quantity,
    name='increase_quantity'),
    path(
    'decrease/<int:cart_id>/',
    views.decrease_quantity,
    name='decrease_quantity'),
    path(
    'remove/<int:cart_id>/',
    views.remove_from_cart,
    name='remove_from_cart'),
    path("logout/", views.user_logout, name="logout"),
    #path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.payment, name="payment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
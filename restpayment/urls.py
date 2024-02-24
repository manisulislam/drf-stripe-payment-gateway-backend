from .views import ProductPreview,CreateStripeCheckoutSession
from django.urls import path

urlpatterns=[
    path('product/<int:pk>',ProductPreview.as_view(),name='product-preview'),
    path('create-checkout-session/<int:pk>/', CreateStripeCheckoutSession.as_view(), name='create-checkout-session'),
]
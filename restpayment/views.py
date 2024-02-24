from django.shortcuts import render
from .serializers import ProductSerializers
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
import stripe
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductPreview(RetrieveAPIView):
    serializer_class = ProductSerializers
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()

class CreateStripeCheckoutSession(APIView):
    def post(self,requst,*args, **kwargs):
        prod_id=self.kwargs['pk']
        try:
            product=Product.objects.get(id=prod_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data':{
                            'currency':'usd',
                            'unit_amount':int(product.price)*100,
                            'product_data':{
                                'name':product.name,
                            }
                        },
                        'quantity':1,
                    }
                ],
                mode='payment',
                metadata={
                    'product_id':product.id,
                },
                success_url=settings.SITE_URL+'?success=True',
                cancel_url=settings.SITE_URL+'?cancel=True',

            )
            return redirect(checkout_session.url)

        except Exception as e:
            return Response({
                'msg':'Something went wrong while creating stripe session',
                'error':str(e),
                
                },status=status.HTTP_400_BAD_REQUEST)

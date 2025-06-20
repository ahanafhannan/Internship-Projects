from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage),
    path('homepage/' , views.homepage),
    path('grant/', views.grant),
    path('execute/',views.execute),
    path('create_agreement/',views.create_agreement),
    path('execute_agreement/',views.execute_agreement),
    path('pay_with_agreement/',views.pay_with_agreement),
    path('cancel_agreement/',views.cancel_agreement),
    path('single-product.html/',views.payment),
    path('single-product_agg.html/',views.payment)
]
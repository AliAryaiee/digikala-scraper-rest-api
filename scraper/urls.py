from django.urls import path
from . import views

urlpatterns = [
    path("", views.SingleProductView.as_view(), name="single-product"),
    path("list", views.ListProductsView.as_view(), name="products-list"),
]

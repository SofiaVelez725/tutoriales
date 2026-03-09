from django.urls import path

from .views import (
    AboutPageView,
    ContactPageView,
    HomePageView,
    ProductCreateView,
    ProductCreatedView,
    ProductIndexView,
    ProductShowView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("products/", ProductIndexView.as_view(), name="index"),
    path("products/create", ProductCreateView.as_view(), name="form"),
    path("products/created/", ProductCreatedView.as_view(), name="product-created"),
    path("products/<str:id>", ProductShowView.as_view(), name="show"),
]

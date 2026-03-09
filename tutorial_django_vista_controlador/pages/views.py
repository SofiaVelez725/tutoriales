from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import Product


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Online Store"
        context["subtitle"] = "Welcome"
        return context


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "About us - Online Store"
        context["subtitle"] = "About us"
        context["description"] = "about us: texto de relleno porque no quiero generar uno"
        context["author"] = "developed by: sofia y co"
        return context


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contact - Online Store"
        context["subtitle"] = "Contact"
        context["email"] = "emailDeRelleno@dormir.co"
        context["address"] = "carrera 67 #69 420 sur"
        context["phone"] = "420 666 6767"
        return context


class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        view_data = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all(),
        }
        return render(request, self.template_name, view_data)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse("home"))

        view_data = {
            "title": product.name + " - Online Store",
            "subtitle": product.name + " - Product information",
            "product": product,
        }
        return render(request, self.template_name, view_data)


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        view_data = {
            "title": "Create product",
            "form": form,
        }
        return render(request, self.template_name, view_data)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product-created")

        view_data = {
            "title": "Create product",
            "form": form,
        }
        return render(request, self.template_name, view_data)


class ProductCreatedView(TemplateView):
    template_name = "products/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product created - Online Store"
        context["subtitle"] = "Product created"
        return context


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context

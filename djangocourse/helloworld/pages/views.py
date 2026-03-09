from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView


class HomePageView(TemplateView):
	template_name = 'pages/home.html'


class AboutPageView(TemplateView):
	template_name = 'pages/about.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(
			{
				'title': 'About us - Online Store',
				'subtitle': 'About us',
				'description': 'about us: texto de relleno porque no quiero generar uno',
				'author': 'developed by: sofia y co',
			}
		)
		return context


class ContactPageView(TemplateView):
	template_name = 'pages/contact.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(
			{
				'title': 'Contact - Online Store',
				'subtitle': 'Contact',
				'email': 'emailDeRelleno@dormir.co',
				'address': 'carrera 67 #69 420 sur',
				'phone': '420 666 6767',
			}
		)
		return context


class Product:
	products = [
		{'id': '1', 'name': 'TV', 'description': 'Best TV', 'price': 450.0},
		{'id': '2', 'name': 'iPhone', 'description': 'Best iPhone', 'price': 1200.0},
		{'id': '3', 'name': 'Chromecast', 'description': 'Best Chromecast', 'price': 90.0},
		{'id': '4', 'name': 'Glasses', 'description': 'Best Glasses', 'price': 45.0},
	]


class ProductIndexView(View):
	template_name = 'products/index.html'

	def get(self, request):
		view_data = {
			'title': 'Products - Online Store',
			'subtitle': 'List of products',
			'products': Product.products,
		}
		return render(request, self.template_name, view_data)


class ProductShowView(View):
	template_name = 'products/show.html'

	def get(self, request, id):
		if not id.isdigit():
			return HttpResponseRedirect(reverse('home'))

		index = int(id) - 1
		if index < 0 or index >= len(Product.products):
			return HttpResponseRedirect(reverse('home'))

		product = Product.products[index]
		view_data = {
			'title': product['name'] + ' - Online Store',
			'subtitle': product['name'] + ' - Product information',
			'product': product,
		}
		return render(request, self.template_name, view_data)


class ProductForm(forms.Form):
	name = forms.CharField(required=True)
	price = forms.FloatField(required=True)

	def clean_price(self):
		price = self.cleaned_data['price']
		if price <= 0:
			raise forms.ValidationError('Price must be greater than zero.')
		return price


class ProductCreateView(View):
	template_name = 'products/create.html'

	def get(self, request):
		form = ProductForm()
		view_data = {'title': 'Create product', 'form': form}
		return render(request, self.template_name, view_data)

	def post(self, request):
		form = ProductForm(request.POST)
		if form.is_valid():
			view_data = {
				'title': 'Product created - Online Store',
				'subtitle': 'Product created',
				'name': form.cleaned_data['name'],
				'price': form.cleaned_data['price'],
			}
			return render(request, 'products/success.html', view_data)

		view_data = {'title': 'Create product', 'form': form}
		return render(request, self.template_name, view_data)

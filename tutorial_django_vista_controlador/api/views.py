from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

from pages.models import Product
from todo.models import ToDo

from .serializers import ProductSerializer, ToDoSerializer, ToDoToggleCompleteSerializer


class ToDoListCreate(generics.ListCreateAPIView):
	serializer_class = ToDoSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return ToDo.objects.filter(user=user).order_by("-created")

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ToDoSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return ToDo.objects.filter(user=user)


class ToDoToggleComplete(generics.UpdateAPIView):
	serializer_class = ToDoToggleCompleteSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return ToDo.objects.filter(user=user)

	def perform_update(self, serializer):
		serializer.instance.completed = not serializer.instance.completed
		serializer.save()


class ProductList(generics.ListAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.all().order_by("-created_at")


@csrf_exempt
def signup(request):
	if request.method == "POST":
		try:
			data = JSONParser().parse(request)
			user = User.objects.create_user(
				username=data["username"],
				password=data["password"],
			)
			user.save()
			token = Token.objects.create(user=user)
			return JsonResponse({"token": str(token)}, status=201)
		except IntegrityError:
			return JsonResponse(
				{"error": "username taken. choose another username"},
				status=400,
			)

	return JsonResponse({"error": "method not allowed"}, status=405)


@csrf_exempt
def login(request):
	if request.method == "POST":
		data = JSONParser().parse(request)
		user = authenticate(
			request,
			username=data["username"],
			password=data["password"],
		)
		if user is None:
			return JsonResponse(
				{"error": "unable to login. check username and password"},
				status=400,
			)

		try:
			token = Token.objects.get(user=user)
		except Token.DoesNotExist:
			token = Token.objects.create(user=user)

		return JsonResponse({"token": str(token)}, status=201)

	return JsonResponse({"error": "method not allowed"}, status=405)

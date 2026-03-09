from rest_framework import serializers

from pages.models import Product
from todo.models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = ToDo
        fields = ["id", "title", "memo", "created", "completed"]


class ToDoToggleCompleteSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField(required=False)

    class Meta:
        model = ToDo
        fields = ["completed"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "created_at", "updated_at"]

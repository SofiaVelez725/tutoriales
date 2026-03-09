from django.contrib import admin

from .models import Comment, Product

admin.site.register(Product)
admin.site.register(Comment)

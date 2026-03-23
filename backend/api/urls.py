from django.contrib import admin
from django.urls import path,include
from .views import Todoviewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'todo', Todoviewset, basename='todo')

urlpatterns = [
    path('api/' , include(router.urls), name='api'),
]

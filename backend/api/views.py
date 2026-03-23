from rest_framework import viewsets, permissions # 1. Ajoute "permissions" ici
from .models import Todo
from .serializer import TodoSerializer

class Todoviewset(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
 

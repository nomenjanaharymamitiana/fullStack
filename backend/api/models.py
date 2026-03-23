import uuid

from django.db import models
 
 
class Todo(models.Model):
    #creer une modele pour la list de todo
    id_todo= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_todo = models.CharField(max_length=50)
    dateCreate = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom_todo
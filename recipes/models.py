from django.db import models
from djongo import models as djongo_models

class Recipe(models.Model):
    """Model for storing recipe information"""
    # Use ObjectIdField as the primary key for MongoDB compatibility
    id = djongo_models.ObjectIdField(primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Field to store the embedding vector
    embedding = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.title

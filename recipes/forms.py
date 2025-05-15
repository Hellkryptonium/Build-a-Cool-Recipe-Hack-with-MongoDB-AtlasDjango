from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """Form for creating and editing recipes"""
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'cooking_time', 'servings', 'category']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter ingredients, one per line'}),
            'instructions': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Enter cooking instructions'}),
        }

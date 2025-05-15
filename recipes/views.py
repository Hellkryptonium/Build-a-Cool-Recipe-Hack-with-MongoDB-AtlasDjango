from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.utils import DatabaseError
from bson import ObjectId
from .models import Recipe
from .forms import RecipeForm
from .utils import generate_recipe_embedding, get_recipe_suggestions
import json

def home(request):
    """Home page view that displays all recipes"""
    all_recipes = Recipe.objects.all()
    print(f"DEBUG: Retrieved {all_recipes.count()} recipes from the database.")
    
    # Filter out recipes that might have a None pk
    recipes_with_pk = []
    invalid_recipes_count = 0
    for recipe in all_recipes:
        if recipe.pk is not None:
            recipes_with_pk.append(recipe)
        else:
            invalid_recipes_count += 1
            print(f"Warning: Recipe '{recipe.title if hasattr(recipe, 'title') else 'Untitled'}' found with pk=None.")

    if invalid_recipes_count > 0:
        print(f"Warning: {invalid_recipes_count} recipe(s) were filtered out from home page due to missing PK.")
    
    print(f"DEBUG: Displaying {len(recipes_with_pk)} recipes on the home page.")
    return render(request, 'recipes/home.html', {'recipes': recipes_with_pk})

def recipe_detail(request, pk):
    """View for a single recipe"""
    try:
        object_id = ObjectId(pk)
    except Exception:
        # If pk is not a valid ObjectId, raise 404
        from django.http import Http404
        raise Http404("Invalid recipe ID.")
    recipe = get_object_or_404(Recipe, pk=object_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def add_recipe(request):
    """View to add a new recipe"""
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            # Create but don't save the new recipe instance yet
            recipe = form.save(commit=False)
            # Generate embedding for the ingredients
            try:
                recipe.embedding = generate_recipe_embedding(recipe.ingredients)
            except Exception as e:
                print(f"Error generating embedding: {e}")
                recipe.embedding = None
            # Save the recipe (no transaction.atomic for MongoDB)
            try:
                recipe.save()
                print(f"DEBUG: Saved recipe with pk={recipe.pk} and id={getattr(recipe, 'id', None)}")
                exists = Recipe.objects.filter(pk=recipe.pk).exists()
                print(f"DEBUG: Recipe exists in DB after save? {exists}")
                return redirect('recipe_detail', pk=str(recipe.pk))
            except Exception as save_err:
                print(f"Error saving recipe: {save_err}")
                form.add_error(None, f"Error saving recipe: {save_err}")
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

def edit_recipe(request, pk):
    """View to edit an existing recipe"""
    try:
        object_id = ObjectId(pk)
    except Exception:
        from django.http import Http404
        raise Http404("Invalid recipe ID.")
    recipe = get_object_or_404(Recipe, pk=object_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            # Update embedding if ingredients changed
            if 'ingredients' in form.changed_data:
                try:
                    recipe.embedding = generate_recipe_embedding(recipe.ingredients)
                except Exception as e:
                    print(f"Error generating embedding: {e}")
                    recipe.embedding = None
            recipe.save()
            return redirect('recipe_detail', pk=str(recipe.pk))
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'edit': True, 'recipe': recipe})

def delete_recipe(request, pk):
    """View to delete a recipe"""
    try:
        object_id = ObjectId(pk)
    except Exception:
        from django.http import Http404
        raise Http404("Invalid recipe ID.")
    recipe = get_object_or_404(Recipe, pk=object_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('home')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def get_recommendations(request, pk):
    """View to get recipe recommendations based on a recipe"""
    try:
        object_id = ObjectId(pk)
    except Exception:
        from django.http import Http404
        raise Http404("Invalid recipe ID.")
    recipe = get_object_or_404(Recipe, pk=object_id)
    
    # Get recipe suggestions using Google Gemini
    suggestions = get_recipe_suggestions(recipe)
    
    return JsonResponse(suggestions, safe=False)

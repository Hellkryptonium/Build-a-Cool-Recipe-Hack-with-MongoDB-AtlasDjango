import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_app.settings')
django.setup()

from recipes.models import Recipe
from recipes.utils import generate_recipe_embedding

# Sample recipes
SAMPLE_RECIPES = [
    {
        "title": "Classic Spaghetti Carbonara",
        "category": "Italian",
        "ingredients": """200g spaghetti
100g pancetta or guanciale
2 large eggs
50g pecorino cheese, grated
50g parmesan cheese, grated
2 cloves garlic, minced
Salt and black pepper to taste""",
        "instructions": """1. Cook spaghetti in salted boiling water according to package instructions until al dente.
2. While pasta is cooking, heat a large skillet over medium heat and cook the pancetta until crispy, about 5 minutes.
3. In a bowl, whisk together eggs, grated cheeses, and black pepper.
4. Reserve 1/2 cup of pasta water, then drain the pasta.
5. Add hot pasta to the skillet with pancetta, tossing to coat in the rendered fat.
6. Remove from heat and quickly add the egg mixture, tossing constantly. Add a splash of pasta water to create a creamy sauce.
7. Serve immediately with extra grated cheese and black pepper.""",
        "cooking_time": 20,
        "servings": 2
    },
    {
        "title": "Thai Green Curry",
        "category": "Thai",
        "ingredients": """400ml coconut milk
4 tbsp green curry paste
500g chicken breast, sliced
1 red bell pepper, sliced
1 zucchini, sliced
1 small eggplant, cubed
Handful of Thai basil leaves
2 kaffir lime leaves
1 tbsp fish sauce
1 tbsp brown sugar
1 tbsp vegetable oil""",
        "instructions": """1. Heat the oil in a large pan or wok over medium heat.
2. Add the curry paste and cook for 1-2 minutes until fragrant.
3. Add the chicken and stir until coated with the paste.
4. Pour in the coconut milk, add the kaffir lime leaves, and bring to a simmer.
5. Add the vegetables and simmer for 10-15 minutes until the chicken is cooked through and vegetables are tender.
6. Stir in the fish sauce and brown sugar.
7. Remove from heat and stir in the Thai basil leaves.
8. Serve with jasmine rice.""",
        "cooking_time": 30,
        "servings": 4
    },
    {
        "title": "Quick Avocado Toast",
        "category": "Breakfast",
        "ingredients": """2 slices whole grain bread
1 ripe avocado
1 small lime, juiced
Salt and pepper to taste
Red pepper flakes (optional)
2 eggs (optional)""",
        "instructions": """1. Toast the bread slices until golden and crisp.
2. Cut the avocado in half, remove the pit, and scoop the flesh into a bowl.
3. Add lime juice, salt, and pepper. Mash with a fork to desired consistency.
4. Spread the avocado mixture on the toast.
5. If desired, top with a fried or poached egg.
6. Sprinkle with red pepper flakes if using.""",
        "cooking_time": 10,
        "servings": 1
    }
]

def load_sample_data():
    """Load sample recipe data into the database"""
    print("Loading sample recipe data...")
    
    # Clear existing recipes
    Recipe.objects.all().delete()
    
    for recipe_data in SAMPLE_RECIPES:
        # Generate embedding for the ingredients
        embedding = generate_recipe_embedding(recipe_data['ingredients'])
        
        # Create and save the recipe
        recipe = Recipe(
            title=recipe_data['title'],
            category=recipe_data['category'],
            ingredients=recipe_data['ingredients'],
            instructions=recipe_data['instructions'],
            cooking_time=recipe_data['cooking_time'],
            servings=recipe_data['servings'],
            embedding=embedding
        )
        recipe.save()
        print(f"Added recipe: {recipe.title}")
    
    print(f"Successfully loaded {len(SAMPLE_RECIPES)} sample recipes.")

if __name__ == "__main__":
    load_sample_data()

import os
from django.core.management.base import BaseCommand
from recipes.models import Recipe
from recipes.utils import generate_recipe_embedding
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Command(BaseCommand):
    help = 'Loads sample recipe data into the database and generates embeddings'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting existing recipes...'))
        Recipe.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing recipes deleted.'))

        sample_recipes = [
            {
                'title': 'Spaghetti Carbonara',
                'ingredients': 'Spaghetti, Eggs, Pancetta, Pecorino Romano Cheese, Black Pepper',
                'instructions': '1. Cook spaghetti. 2. Fry pancetta. 3. Whisk eggs and cheese. 4. Combine all with pasta water. 5. Serve with pepper.',
                'category': 'Italian',
                'cooking_time': 20,
                'servings': 4,
            },
            {
                'title': 'Chicken Curry',
                'ingredients': 'Chicken Breast, Onion, Garlic, Ginger, Coconut Milk, Curry Powder, Turmeric, Rice',
                'instructions': '1. Sauté onion, garlic, ginger. 2. Add chicken and spices. 3. Stir in coconut milk. 4. Simmer until chicken is cooked. 5. Serve with rice.',
                'category': 'Indian',
                'cooking_time': 45,
                'servings': 4,
            },
            {
                'title': 'Chocolate Chip Cookies',
                'ingredients': 'Flour, Butter, Sugar, Brown Sugar, Eggs, Vanilla Extract, Chocolate Chips, Baking Soda, Salt',
                'instructions': '1. Cream butter and sugars. 2. Beat in eggs and vanilla. 3. Mix dry ingredients. 4. Stir in chocolate chips. 5. Bake at 375°F (190°C) for 10-12 minutes.',
                'category': 'Dessert',
                'cooking_time': 25,
                'servings': 24,
            },
            {
                'title': 'Classic Tomato Soup',
                'ingredients': 'Tomatoes, Onion, Garlic, Vegetable Broth, Olive Oil, Basil, Salt, Pepper',
                'instructions': '1. Sauté onion and garlic in olive oil. 2. Add chopped tomatoes and broth. 3. Simmer for 20 minutes. 4. Blend until smooth. 5. Season with basil, salt, and pepper. Serve hot.',
                'category': 'Soup',
                'cooking_time': 30,
                'servings': 4,
            },
            {
                'title': 'Guacamole',
                'ingredients': 'Avocados, Lime Juice, Onion, Cilantro, Jalapeño, Salt',
                'instructions': '1. Mash avocados in a bowl. 2. Stir in lime juice, chopped onion, cilantro, and jalapeño. 3. Season with salt. Mix well. Serve with chips.',
                'category': 'Appetizer',
                'cooking_time': 10,
                'servings': 6,
            }
        ]

        self.stdout.write(self.style.SUCCESS(f'Loading {len(sample_recipes)} sample recipes...'))
        voyage_api_key = os.getenv('VOYAGE_API_KEY')
        if not voyage_api_key:
            self.stdout.write(self.style.ERROR('VOYAGE_API_KEY not found in .env file. Cannot generate embeddings.'))
            return

        for recipe_data in sample_recipes:
            try:
                embedding = generate_recipe_embedding(recipe_data['ingredients'])
                if embedding:
                    # Create the recipe instance
                    recipe_instance = Recipe.objects.create(
                        title=recipe_data['title'],
                        ingredients=recipe_data['ingredients'],
                        instructions=recipe_data['instructions'],
                        category=recipe_data['category'],
                        cooking_time=recipe_data['cooking_time'],
                        servings=recipe_data['servings'],
                        embedding=embedding
                    )
                    # Check if pk is assigned
                    if recipe_instance and recipe_instance.pk:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added recipe: "{recipe_instance.title}" with PK: {recipe_instance.pk}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Added recipe "{recipe_data["title"]}" BUT ITS PK IS None or invalid.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Could not generate embedding for "{recipe_data["title"]}". Skipping.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding recipe "{recipe_data["title"]}": {e}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data loading complete.'))


from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'cooking_time', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'ingredients')
    readonly_fields = ('embedding',)

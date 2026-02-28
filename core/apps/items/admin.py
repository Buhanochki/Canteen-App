from django.contrib import admin

from core.apps.items.models import Item, IngredientItem
from django.utils.html import format_html

class IngredientItemInline(admin.TabularInline):
    model = IngredientItem
    extra = 1
    min_num = 0
    
    fields = ['ingredient', 'amount']
    


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "display_ingredients",
        "created_at",
        "updated_at",
    )
    
    exclude = ('ingredients',)
    
    inlines = [IngredientItemInline]
    
    def display_ingredients(self, obj):
        item_ingredients = obj.ingredientitem_set.select_related('ingredient').all()
        
        if not item_ingredients:
            return format_html('<span style="color: #999; font-style: italic;">Нет ингредиентов</span>')
        
        display_items = []
        for ii in item_ingredients[:3]:
            display_items.append(f"{ii.ingredient.title} ({ii.amount})")
        
        tooltip_items = []
        for ii in item_ingredients:
            tooltip_items.append(f"• {ii.ingredient.title}: {ii.amount}")
        
        display_text = ", ".join(display_items)
        
        if item_ingredients.count() > 3:
            display_text += f" (+{item_ingredients.count() - 3})"
        
        return format_html(
            '<span style="cursor: help;" title="{}">{}</span>',
            "\n".join(tooltip_items), 
            display_text
        )
    
    display_ingredients.short_description = "Ингредиенты"





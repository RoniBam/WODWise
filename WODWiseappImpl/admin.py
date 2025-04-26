from django.contrib import admin


from .models import Box, Review

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_month', 'open_gym')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('box', 'user', 'rating', 'created_at')
    list_filter = ('box', 'user', 'rating')
    search_fields = ('box__name', 'user__username', 'comment')


from django.contrib import admin
from .models import Cat, Achievement, AchievementCat


class AchievementCatInline(admin.TabularInline):
    model = AchievementCat
    extra = 1


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'birth_year', 'owner', 'created_at')
    list_filter = ('color', 'birth_year', 'created_at')
    search_fields = ('name', 'owner__username')
    inlines = [AchievementCatInline]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
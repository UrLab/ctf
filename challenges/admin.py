from django.contrib import admin

from .models import Category, Challenge, Hint, Resolution

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass

@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    pass

@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    pass

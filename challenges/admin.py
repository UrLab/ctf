from django.contrib import admin

from .models import Category, Challenge, Hint, Resolution, Phase


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'category', 'attachment', 'phase')
    list_filter = ('category', 'points', 'phase')


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('text', 'visible', 'challenge')
    list_filter = ('visible',)


@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    list_display = ('team', 'challenge', 'time')
    list_filter = ('challenge', 'time')


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'stop', 'slug')
    prepopulated_fields = {'slug': ('name',), }

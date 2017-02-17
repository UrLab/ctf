from django.contrib import admin

from .models import Category, Challenge, Hint, Resolution, Phase, Attempt, Sponsor


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'points', 'category', 'attachment', 'phase', 'sponsor')
    list_filter = ('category', 'points', 'phase', 'sponsor')


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


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'distance', 'user', 'team', 'challenge', 'time',)
    list_filter = ('challenge', )

    def team(self, attempt):
        return attempt.user.team


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass

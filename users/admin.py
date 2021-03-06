from django.contrib import admin
from .models import User, Team, Affiliation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'team', 'email', 'created', 'first_name', 'last_name', 'affiliation')
    list_filter = ('team', 'affiliation')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('proof_token', )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'hidden', 'is_orga', 'score', 'size', 'pretty_affiliations')

    def pretty_affiliations(self, team):
        return ', '.join([str(x) for x in team.affiliations])


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass

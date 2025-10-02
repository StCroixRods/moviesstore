from django.contrib import admin
from .models import Petition

class PetitionAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'user', 'total_votes')
    search_fields = ['movie_name', 'user__username']

    def total_votes(self, obj):
        return obj.total_votes()
    total_votes.short_description = 'Total Votes'

admin.site.register(Petition, PetitionAdmin)